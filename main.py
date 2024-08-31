from src.email_fetcher import fetch_emails
from src.model_setup import setup_llama_model
from src.summarizer import summarize_email

def main():
    tokenizer, model = setup_llama_model()
    emails = fetch_emails(10)  # Fetch the last 10 emails
    
    summaries = []
    for email in emails:
        summary = summarize_email(email, tokenizer, model)
        summaries.append({
            "subject": email["subject"],
            "summary": summary
        })
    
    # Print summaries
    for summary in summaries:
        print(f"Subject: {summary['subject']}")
        print(f"Summary: {summary['summary']}")
        print("-" * 50)

if __name__ == "__main__":
    main()