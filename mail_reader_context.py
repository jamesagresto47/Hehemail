from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForCausalLM

from onprem import LLM
import re
import json


# Load conversation history from the file if it exists
def load_history(history_file):
    try:
        with open(history_file, 'r') as file:
            return json.load(file)[-5:]
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return an empty list if file does not exist or is empty

# Save conversation history to the file


def save_history(history_file, history):
    with open(history_file, 'w') as file:
        json.dump(history[-5:], file, indent=4)


def clean_body(body):
    return re.sub(r'\n+\r+\t+', '. ', body)


def summarize_and_remember(summarizer, user_input, history_file, history):
    context = "\n".join(history)
    full_input = f"""
        Summarize this:
        Current Email Body: {user_input}
        Context of Recent Email Bodies: {context}
        Turn it into a slightly funny podcast
    """

    print(full_input)

    # Summarize the user input
    answer = summarizer.prompt(full_input)

    hist_addition = {
        "Body": user_input,
        "Context": context,
        "Answer": answer
    }

    return hist_addition


def main():
    history_file = 'email_history.json'
    convo_data = load_history(history_file)
    convo_history = json.dumps(convo_data)

    gmail_bodys = []
    with open("gmail_today.json", 'r') as f:
        data = json.load(f)
        print(data)

        for obj in data:
            body = obj['Body']
            if len(body) < 512:
                gmail_bodys.append(body)

    if len(gmail_bodys) == 0:
        print("No Emails Found")
        exit()

    summarizer = LLM()
    summaries = []

    for body in gmail_bodys:
        body = clean_body(body)
        summary = summarize_and_remember(
            summarizer, body, history_file, convo_history)
        # print(summary)
        # print("=" * 50)
        summaries.append(summary)
        convo_data.append(summary)

    # Save the updated conversation history
    save_history(history_file, summaries)


if __name__ == "__main__":
    main()
