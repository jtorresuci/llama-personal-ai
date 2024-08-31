import os
import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv
from src.model_setup import setup_llama_model
from src.summarizer import summarize_email

# Load environment variables
load_dotenv()

def fetch_emails(num_emails=10):
    # Gmail IMAP settings
    imap_server = "imap.gmail.com"
    email_address = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_APP_PASSWORD")

    if not email_address or not password:
        raise ValueError("Email address or password not set in .env file")

    # Connect to the Gmail IMAP server
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(email_address, password)
    mail.select("inbox")

    # Search for emails
    _, message_numbers = mail.search(None, "ALL")
    email_ids = message_numbers[0].split()

    emails = []
    for num in email_ids[-num_emails:]:  # Get the last num_emails
        _, msg = mail.fetch(num, "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                email_message = email.message_from_bytes(response[1])
                subject, encoding = decode_header(email_message["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8")
                sender = email_message["From"]
                body = ""
                if email_message.is_multipart():
                    for part in email_message.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                else:
                    body = email_message.get_payload(decode=True).decode()
                
                emails.append({"subject": subject, "sender": sender, "body": body})

    mail.close()
    mail.logout()
    return emails

def main():
    # Fetch the latest 10 emails
    emails = fetch_emails(10)

    # Load the model and tokenizer
    tokenizer, model = setup_llama_model()

    # Summarize each email
    for email_content in emails:
        print("Original Email:")
        print(f"Subject: {email_content['subject']}")
        print(f"From: {email_content['sender']}")
        print(f"Body: {email_content['body']}\n")

        summary = summarize_email(email_content, tokenizer, model)
        print("Summary:")
        print(summary)
        print("="*50)

if __name__ == "__main__":
    main()
