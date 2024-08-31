from flask import Flask, request, jsonify
from model_setup import setup_llama_model
from summarizer import summarize_email

app = Flask(__name__)

# Load the model and tokenizer during server startup
tokenizer, model = setup_llama_model()

@app.route('/summarize', methods=['POST'])
def summarize():
    email_content = request.json
    summary = summarize_email(email_content, tokenizer, model)
    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
