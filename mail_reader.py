from onprem import LLM
import re
import json


def clean_body(body):
    return re.sub(r'\n+\r+\t+', '. ', body)


def mail_reader(data):
    gmail_bodys = []
    gmail_subjs = []
    with open("gmail_today.json", 'r') as f:
        # data = json.load(f)
        # print(data)

        for obj in data:
            body = obj['Body']
            if len(body) < 2800:
                gmail_bodys.append(body)
                gmail_subjs.append(obj["Subject"])

    if len(gmail_bodys) == 0:
        print("No Emails Found")
        exit()

    summarizer = LLM(n_gpu_layers=-1, verbose=False, temperature=2)
    summaries = []

    for i in range(len(gmail_bodys)):
        print(f"Current Subject: {gmail_subjs[i]}")

        body = clean_body(gmail_bodys[i])
        # print(body)
        full_input = f"Pretend you are a news anchor covering a story. Summarize this current email body: {body} and turn it into a slightly funny breaking news broadcast in under 3 sentences. Do not explain he context of the sayings, such as \"[Breaking news voice]\" and start it with \"BREAKING NEWS\". Do not include hashtags, emoji, or anything else other than plaintext, and just act as if you were a news anchor."
        summaries.append({f"Email {i}": summarizer.prompt(full_input)})

    return summaries

    with open("hehemail.json", "w") as f:
        json.dump(summaries, f, indent=4)


if __name__ == "__main__":
    mail_reader()
