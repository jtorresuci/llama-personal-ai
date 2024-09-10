from flask import Flask, request, jsonify
from summarizer import summarize_email
import requests

app = Flask(__name__)

MODEL_SERVER_URL = "http://localhost:5001/prompt"

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        email_content = request.json
        summary = summarize_email(email_content)
        return jsonify({"summary": summary}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        messages = request.json.get('messages')
        user_message = messages[-1]['content']  # Get the last user message
        prompt = f"'{user_message}"  # Clear prompt structure
        response = requests.post(MODEL_SERVER_URL, json={"prompt": prompt})  # Send as prompt
        model_response = response.json().get('response', '')  # Get the model's response
        return jsonify({"response": model_response}), response.status_code  # Return only the model's response
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)