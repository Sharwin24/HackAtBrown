import torch
from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM

class Transformer:
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    def predict(self, input_prompt:str, context: str):
        
        inputs = self.tokenizer(f"{input_prompt} {context}", return_tensors="pt")
        inputs = {name: tensor.to(self.device) for name, tensor in inputs.items()}
        with torch.no_grad():
            outputs = self.model(**inputs)

        logits = outputs.logits
        return logits

class Embedder:
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        
    def last_token_pool(self, last_hidden_states: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        left_padding = (attention_mask[:, -1].sum() == attention_mask.shape[0])
        if left_padding:
            return last_hidden_states[:, -1]
        else:
            sequence_lengths = attention_mask.sum(dim=1) - 1
            batch_size = last_hidden_states.shape[0]
            return last_hidden_states[torch.arange(batch_size, device=last_hidden_states.device), sequence_lengths]
    
    def embed(self, texts:str):
        # Tokenization: Encode the inputs
        inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        inputs = {name: tensor.to(self.device) for name, tensor in inputs.items()}
        # Model Inference: Get the embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)
        # Get the last hidden states
        last_hidden_states = outputs.last_hidden_state
        # Extract the embedding for the [CLS] token (the first token)
        cls_embedding = last_hidden_states[:, 0, :]
        last_hidden_state=self.last_token_pool(last_hidden_state, inputs['attention_mask'])
        print(last_hidden_state.shape)
        return last_hidden_state #cls_embedding
    
    def train(self, texts):
        # Tokenization: Encode the inputs
        inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        inputs = {name: tensor.to(self.device) for name, tensor in inputs.items()}
        # Model Inference: Get the embeddings
        outputs = self.model(**inputs)
        # Get the last hidden states
        embeddings = outputs.last_hidden_state
        cls_embedding=embeddings[:,0,:]
        
        return cls_embedding
