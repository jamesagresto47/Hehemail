import imaplib
import email
import re
import json
import os
from collections import Counter
from dotenv import load_dotenv

EXCLUDED_SENDERS = ["LinkedIn <messages-noreply@linkedin.com>",
                    "LinkedIn <notifications-noreply@linkedin.com>", 
                    "LinkedIn Job Alerts <jobalerts-noreply@linkedin.com>", 
                    "\"Ticketmaster\" <newsletter@email.ticketmaster.com>",
                    "\"Duolingo\" <hello@duolingo.com>",
                    "\"Facebook\" <groupupdates@facebookmail.com>"
                    "Venmo <venmo@venmo.com>",
                    "Google <no-reply@accounts.google.com>",
                    "NokiaME DoNotReply <donotreply.nokiaME@people.nokia.com>",
                    "IBM Careers <talent@ibm.com>",
                    "LinkedIn News <editors-noreply@linkedin.com>", 
                    "\"Fanatics.com\" <shop@e.fanatics.com>",
                    'LinkedIn <jobs-listings@linkedin.com>']
EXCLUDED_KEYWORDS_SUBJECT = []
EXCLUDED_KEYWORDS_BODY = []


def remove_links(text):
    """Removes URLs from the provided text using a regular expression."""
    # Regular expression to identify URLs
    url_pattern = re.compile(r'http[s]?://\S+|www\.\S+')
    return url_pattern.sub('', text)


def get_email_body(msg):
    """Extracts the plain-text body from an email message object (msg) and excludes HTML content."""
    body = ""
    if msg.is_multipart():  # If email has multiple parts (plain text, HTML, attachments)
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            # Look for the plain text part only and ignore attachments or HTML
            if content_type == "text/plain" and "attachment" not in content_disposition:
                try:
                    body = part.get_payload(decode=True).decode(
                        "utf-8", errors="replace")
                    # Remove links from the extracted text
                    body = remove_links(body)
                    break  # Stop once plain text part is found
                except Exception:
                    continue
            elif content_type == "text/html":  # Skip HTML parts
                continue
    else:  # If the email is not multipart, just get the payload
        try:
            body = msg.get_payload(decode=True).decode(
                "utf-8", errors="replace")
            body = remove_links(body)  # Remove links from the extracted text
        except Exception as e:
            print(f"Failed to decode single-part email: {e}")

    return body


def should_exclude_email(sender, subject, body):
    """Determines if an email should be excluded based on exclusion lists."""
    # Check if the sender's email address is in the exclusion list
    if any(excluded in sender for excluded in EXCLUDED_SENDERS):
        return True

    # Check if the subject contains any of the excluded keywords
    if any(keyword.lower() in (subject or "").lower() for keyword in EXCLUDED_KEYWORDS_SUBJECT):
        return True

    # Check if the body contains any of the excluded keywords
    if any(keyword.lower() in (body or "").lower() for keyword in EXCLUDED_KEYWORDS_BODY):
        return True

    return False


def get_gmail_objs():

    my_email_user = os.environ["GMAIL"]
    my_email_pass = os.environ["GMAIL_PASS"]

    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    mail.login(my_email_user, my_email_pass)
    mail.select("Inbox")


    status, messages = mail.search(None, "UNSEEN")
    email_ids = messages[0].split()[:10]

    print("Emails Retrieved")

    with open("./gmail_today.json", 'w') as f:
        if not email_ids:
            print("No unread emails found.")
            return None
        else:
            # Loop through unread emails
            senders = []
            jsonObjs = []
            for email_id in email_ids:
                try:
                    # Fetch the email by ID
                    res, msg_data = mail.fetch(email_id, '(RFC822)')
                    raw_email = msg_data[0][1]

                    # Parse the raw email using the email library
                    msg = email.message_from_bytes(raw_email)

                    # Extract email metadata
                    sender = msg['From']
                    subject = msg['Subject']
                    date = msg['Date']

                    # Get the email body
                    email_body = get_email_body(msg)

                    # Check if the email should be excluded
                    if should_exclude_email(sender, subject, email_body):
                        continue

                    senders.append(sender)

                    jsonObj = {
                        "From": sender,
                        "Subject": subject,
                        "Date": date,
                        "Body": email_body.encode('utf-8', errors='replace').decode('utf-8')
                    }
                    jsonObjs.append(jsonObj)
                except Exception:
                    continue

            # json.dump(jsonObjs, f, indent=4)

            print(Counter(senders))

        # Close the connection and logout
        mail.close()
        mail.logout()

        return jsonObjs


if __name__ == "__main__":
    get_gmail()
