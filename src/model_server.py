import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from flask import Flask, request, jsonify

app = Flask(__name__)

# Global variables for model and tokenizer
model = None
tokenizer = None

def load_model():
    global model, tokenizer
    model_name = "meta-llama/Meta-Llama-3.1-70BB"
    
    print("Loading model...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True
    )
    print("Model loaded successfully!")

@app.route('/summarize', methods=['POST'])
def summarize_email():
    prompt = f"""Summarize the following email:

Subject: {email_content['subject']}
From: {email_content['sender']}
Body: {email_content['body']}

Summary:"""
    
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    
    try:
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=100,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                num_return_sequences=1
            )
        
        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Check if 'Summary:' is in the output
        if "Summary:" in summary:
            return summary.split("Summary:")[-1].strip()
        else:
            return summary.strip()  # Return the whole output if 'Summary:' is not found
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return "Error: Unable to generate summary."

if __name__ == '__main__':
    load_model()
    app.run(host='0.0.0.0', port=5000)
