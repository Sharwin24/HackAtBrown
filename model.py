import numpy as np 
import torch
## EMBEDDING CLASS
from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM

class Transformer:
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
    
    def predict(self, input_prompt:str, context: str):
        inputs = input_prompt + " " + context
        inputs = self.tokenizer(inputs, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model(**inputs)

        logits = outputs.logits
        return logits

class Embedder:
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def embed(self, texts):
        # Tokenization: Encode the inputs
        inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        # Model Inference: Get the embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)
        # Get the last hidden states
        embeddings = outputs.last_hidden_state
        return embeddings

# # Usage Example
# embedder = Embedder("microsoft/codebert-base")

# # Combining tokens with special tokens
# nl_tokens = embedder.tokenizer.tokenize("return maximum value")
# code_tokens = embedder.tokenizer.tokenize("def max(a,b): if a>b: return a else return b")
# tokens = [embedder.tokenizer.cls_token] + nl_tokens + [embedder.tokenizer.sep_token] + code_tokens + [embedder.tokenizer.sep_token]

# # Getting embeddings
# embeddings = embedder.embed(" ".join(tokens))
# print(embeddings)


# # Load transformer model and tokenizer
# transformer = Transformer("codellama/CodeLlama-7b-Instruct-hf")
# transformer.predict("What is the maximum value", "def max(a,b): if a>b: return a else return b")
