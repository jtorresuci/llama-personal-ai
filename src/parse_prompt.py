import torch
from email_fetcher import fetch_emails
import requests

def parse_prompt(prompt, tokenizer, model):    
    # Ensure the prompt is a string
    if not isinstance(prompt, str):
        raise ValueError("Invalid prompt format. Expected a string.")

    # Tokenize and generate
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=100,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            num_return_sequences=1
        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Remove the input prompt from the response
    response = response[len(prompt):].strip()
    
    return response
