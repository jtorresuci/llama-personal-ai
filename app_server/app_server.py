from flask import Flask, request, jsonify
from summarizer import summarize_email

app = Flask(__name__)

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        email_content = request.json
        summary = summarize_email(email_content)
        return jsonify({"summary": summary}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)