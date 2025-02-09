import os
import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv
from bs4 import BeautifulSoup

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

    # Get the fetch command from environment variable, default to "(RFC822)" if not set
    fetch_command = os.getenv("EMAIL_FETCH_COMMAND", "(RFC822)")

    emails = []
    for num in email_ids[-num_emails:]:  # Get the last num_emails
        _, msg = mail.fetch(num, fetch_command)
        for response in msg:
            if isinstance(response, tuple):
                email_message = email.message_from_bytes(response[1])
                subject, encoding = decode_header(email_message["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8")
                sender = email_message["From"]
                body = ""
                
                # Check if email is multipart
                if email_message.is_multipart():
                    for part in email_message.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))

                        # Extract plain text part
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            body = part.get_payload(decode=True).decode()
                        # Extract HTML part and convert to text
                        elif content_type == "text/html":
                            html_content = part.get_payload(decode=True).decode()
                            soup = BeautifulSoup(html_content, "html.parser")
                            body = soup.get_text()

                # If the email is not multipart, handle as a single part
                else:
                    content_type = email_message.get_content_type()
                    if content_type == "text/plain":
                        body = email_message.get_payload(decode=True).decode()
                    elif content_type == "text/html":
                        html_content = email_message.get_payload(decode=True).decode()
                        soup = BeautifulSoup(html_content, "html.parser")
                        body = soup.get_text()

                emails.append({"subject": subject, "sender": sender, "body": body})

    mail.close()
    mail.logout()
    return emails
