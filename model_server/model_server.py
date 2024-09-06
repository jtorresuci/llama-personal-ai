from flask import Flask, request, jsonify
from model_setup import setup_llama_model
from parse_prompt import parse_prompt
import logging


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

print("Loading model...")
tokenizer, model = setup_llama_model()
print("Model loaded successfully")

@app.route('/prompt', methods=['POST'])
def prompt():
    try:
        app.logger.debug(f"Received data: {request.data}")
        data = request.json
        app.logger.debug(f"Parsed JSON: {data}")
        
        if not data or 'prompt' not in data:
            return jsonify({"error": "No prompt provided in JSON data"}), 400
        
        prompt = data['prompt']
        app.logger.debug(f"Extracted prompt: {prompt}")
        
        response = parse_prompt(prompt, tokenizer, model)
        return jsonify({"response": response}), 200
    except ValueError as e:
        app.logger.error(f"ValueError: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": "An internal server error occurred"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)