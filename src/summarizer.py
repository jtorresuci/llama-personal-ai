import torch

def summarize_email(email_content, tokenizer, model):
    prompt = f"Summarize the following email:\n\nSubject: {email_content['subject']}\nFrom: {email_content['sender']}\nBody: {email_content['body']}\n\nSummary:"
    
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
    
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return summary.split("Summary:")[1].strip()