from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

MODEL_SERVER_URL = "http://localhost:5001/prompt"

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        email_content = request.json
        
        # Create the prompt
        prompt = f"Summarize the following email:\n\nSubject: {email_content['subject']}\nFrom: {email_content['sender']}\nBody: {email_content['body']}\n\nSummary:"
        
        # Send the request to the model server
        response = requests.post(MODEL_SERVER_URL, json={"prompt": prompt})
        response.raise_for_status()
        
        summary = response.json()['response']
        return jsonify({"summary": summary}), 200
    
    except requests.RequestException as e:
        return jsonify({"error": f"Error communicating with model server: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)