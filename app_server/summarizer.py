import requests

MODEL_SERVER_URL = "http://localhost:5001/prompt"

def summarize_email(email_content):
    try:
        prompt = f"Summarize the following email:\n\nSubject: {email_content['subject']}\nFrom: {email_content['sender']}\nBody: {email_content['body']}\n\nSummary:"
    except KeyError as e:
        raise ValueError(f"Missing required email field: {str(e)}")
    
    try:
        response = requests.post(MODEL_SERVER_URL, json={"prompt": prompt})
        response.raise_for_status()
        summary = response.json()['response']
        return summary
    except requests.RequestException as e:
        raise Exception(f"Error communicating with model server: {str(e)}")
