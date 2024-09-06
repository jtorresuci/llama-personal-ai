import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from dotenv import load_dotenv
import os

load_dotenv()

def setup_llama_model():
    model_name = os.getenv("AI_MODEL")
    
    if not model_name:
        raise ValueError("AI_MODEL not set in .env file")
    
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
        trust_remote_code=True,
        max_memory={0: "10GB", "cpu": "16GB"}  # Adjust these values based on your system
    )
    
    return tokenizer, model
