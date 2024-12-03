from get_gmail import get_gmail_objs
from mail_reader import mail_reader
from mail_to_mp3 import mail_to_mp3

def main():
    print("Getting Gmail")
    gmail = get_gmail_objs()
    if gmail is None:
        print("No Gmail Found")
        exit(1)
    summaries = mail_reader(gmail)
    mail_to_mp3(summaries)

if __name__ == "__main__":
    main()