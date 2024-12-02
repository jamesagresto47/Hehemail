from transformers import pipeline

# Initialize summarization pipeline
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_email(previous_emails, current_email):
    # Create a formatted prompt separating context and current message
    prompt = (
        "Previous Conversations:\n"
        f"{previous_emails}\n\n"
        "New Email:\n"
        f"{current_email}\n\n"
        "Summary:"
    )
    
    # Generate the summary using the pipeline
    summary = summarizer(prompt, min_length=50, do_sample=False)
    return summary[0]['summary_text']

# Example of previous and current messages
previous_emails = (
    "Email 1: Hi James, I wanted to remind you about the meeting next Friday.\n"
    "Email 2: Sure Bob, I’ll be ready for that meeting, but let’s review the agenda beforehand."
    "Email 4: The meeting should actually be rescheduled for the following friday due to my daughter's concert"
)
current_email = "Email 3: Hey, just following up on our last discussion. Can you send me the agenda for next Friday's meeting?"

# Generate summary
summary = summarize_email(previous_emails, current_email)
print("Summary: ", summary)
