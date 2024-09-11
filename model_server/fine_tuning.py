import torch
from transformers import Trainer, TrainingArguments, AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import get_peft_model, LoraConfig
from datasets import Dataset
from dotenv import load_dotenv
import os
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

def setup_llama_model():
    logging.info("Setting up LLaMA model...")
    
    model_name = os.getenv("AI_MODEL")
    if not model_name:
        raise ValueError("AI_MODEL not set in .env file")
    
    # BitsAndBytesConfig for quantization
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16  # Using bfloat16 for computation
    )

    logging.info("Loading tokenizer and model...")
    
    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Add a pad token if it doesn't exist
    if tokenizer.pad_token is None:
        tokenizer.add_special_tokens({'pad_token': tokenizer.eos_token})  # Use eos_token as pad_token

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,  # Use the quantization config
        device_map="auto",
        trust_remote_code=True,
        max_memory={0: "10GB", "cpu": "16GB"}  # Adjust memory based on your system
    )

    # Resize token embeddings to match the tokenizer (needed after adding special tokens)
    model.resize_token_embeddings(len(tokenizer))

    logging.info("Model and tokenizer setup complete.")
    
    return tokenizer, model


def fine_tune_model(tokenizer, model, train_dataset):
    logging.info("Setting up LoRA configuration and fine-tuning...")

    # Define LoRA configuration for PEFT
    adapter_config = LoraConfig(
        peft_type="lora",  # LoRA type for adapter
        r=16,  # The rank (adjustable based on memory and performance needs)
        lora_alpha=32,  # Scaling factor for LoRA
        lora_dropout=0.1,  # Dropout rate to regularize training
        bias="none"  # Adjust bias as needed, typically "none" for fine-tuning
    )
    
    # Inject the adapter into the model
    model = get_peft_model(model, adapter_config)

    # Define training arguments
    training_args = TrainingArguments(
        output_dir="./fine_tuned_model",
        per_device_train_batch_size=4,  # Adjust batch size to your hardware
        gradient_accumulation_steps=4,
        logging_steps=100,
        num_train_epochs=3,  # Set the number of epochs
        learning_rate=5e-5,  # Adjust learning rate as necessary
        save_strategy="epoch",  # Save model at the end of every epoch
        evaluation_strategy="steps",
        save_total_limit=2,  # Keep only the last 2 models
        fp16=True  # Mixed precision training for performance improvements
    )

    logging.info("Starting training...")

    # Define data collator
    data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model)

    # Define Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        tokenizer=tokenizer,
        data_collator=data_collator  # Use the data collator
    )

    # Train the model
    trainer.train()

    logging.info("Training complete. Saving the model...")

    # Save the fine-tuned model and tokenizer
    model.save_pretrained("./fine_tuned_model")
    tokenizer.save_pretrained("./fine_tuned_model")

    logging.info("Model and tokenizer saved successfully.")


def load_dataset(file_path, tokenizer):
    logging.info(f"Loading dataset from {file_path}...")

    # Load the dataset from a JSONL file
    dataset = []
    with open(file_path, 'r') as f:
        for line in f:
            entry = json.loads(line)
            
            # Combine instruction and context if context is present
            if entry['context']:
                input_text = f"{entry['instruction']} {entry['context']}"
            else:
                input_text = entry['instruction']
            
            # Tokenize input and response
            tokenized_input = tokenizer(
                input_text,  # Concatenate instruction and context as input
                padding='max_length',  # Pad to max length
                truncation=True,  # Truncate if longer than the max sequence length
                return_tensors='pt'  # Return PyTorch tensors
            )
            
            tokenized_response = tokenizer(
                entry['response'],  # Response as the output labels
                padding='max_length',
                truncation=True,
                return_tensors='pt'
            )

            dataset.append({
                'input_ids': tokenized_input['input_ids'].squeeze(0),  # Remove batch dimension
                'attention_mask': tokenized_input['attention_mask'].squeeze(0),
                'labels': tokenized_response['input_ids'].squeeze(0)  # Labels for training
            })

    logging.info(f"Dataset loaded successfully with {len(dataset)} samples.")
    
    return Dataset.from_list(dataset)


if __name__ == "__main__":
    logging.info("Fine-tuning script started.")

    # Set up the model and tokenizer
    tokenizer, model = setup_llama_model()

    # Load the training dataset
    train_dataset = load_dataset("databricks-dolly-15k.jsonl", tokenizer)

    # Fine-tune the model
    fine_tune_model(tokenizer, model, train_dataset)

    logging.info("Fine-tuning script finished.")
