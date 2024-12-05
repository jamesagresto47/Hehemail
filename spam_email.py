import smtplib
import os

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
# start TLS for security
s.starttls()
# Authentication
s.login(os.environ['GMAIL'], os.environ['GMAIL_PASS'])

email_bodies = [
    "Dear Team,\n\nPlease find the attached report for your review. Let me know if you have any questions.\n\nBest regards,\nAlice",
    "Hi John,\n\nI hope this email finds you well. I just wanted to check in on the status of the project. Looking forward to your update.\n\nCheers,\nSarah",
    ]

email_bodies_2 = [
    "Hello,\n\nYour order #12345 has been shipped and is on its way to you. Estimated delivery date: Dec 5, 2024.\n\nThanks,\nCustomer Support",
    "Dear valued customer,\n\nWe’re excited to inform you about our upcoming sale with up to 50% off on selected items! Visit our website to learn more.\n\nWarm regards,\nThe Sales Team",
    "Hi Everyone,\n\nJust a quick reminder about the team meeting scheduled for tomorrow at 10 AM in the conference room. Please be on time.\n\nBest,\nMark",
    "Dear Subscriber,\n\nThank you for signing up for our newsletter! Stay tuned for updates and exclusive content in your inbox.\n\nBest,\nThe Newsletter Team",
    "Dear James,\n\nCongratulations! You have been shortlisted for the next round of interviews. We’ll reach out shortly with further details.\n\nKind regards,\nHR Team",
    "Hi Alex,\n\nCan you please confirm receipt of the package sent last week? It was delivered to your office on Monday.\n\nThanks,\nKevin",
    "Greetings,\n\nThis is a reminder that your subscription will expire in 3 days. Please renew to continue uninterrupted service.\n\nThank you,\nSupport Team",
    "Dear Friend,\n\nHope you're doing well. I came across this article and thought you'd find it interesting. Let me know your thoughts!\n\nBest wishes,\nEmma"
]


for m in email_bodies:
    try:
        # sending the mail
        s.sendmail(os.environ['GMAIL'], os.environ['GMAIL'], m)
    except UnicodeEncodeError:
        continue
# terminating the session
s.quit()
