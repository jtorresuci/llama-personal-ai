from src.email_fetcher import fetch_emails
import requests

def main():
    # Fetch emails
    emails = fetch_emails()
    
    # Server URL for summarization
    server_url = "http://localhost:5000/summarize"  # Adjust the URL as needed
    
    for email in emails:
        # Send request to server for summarization
        response = requests.post(server_url, json=email)
        
        if response.status_code == 200:
            summary = response.json()['summary']
            
            # Output results to console
            print(f"Email from: {email['sender']}")
            print(f"Subject: {email['subject']}")
            print(f"Summary: {summary}")
            print("-" * 50)
        else:
            print(f"Error summarizing email from {email['sender']}: {response.status_code}")

if __name__ == "__main__":
    main()
