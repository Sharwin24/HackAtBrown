##FILE TAKES IN CHATGPT QUESTION ANSWER EMBEDDED PAIRS AND COMPARES IT TO RAG OUTPUT
import torch
import torch.nn.functional as F
import numpy as np
from model import embedder
from model import transformer
from torch.utils.data import DataLoader



"""
Computes a MultipleNegativeRankingLoss function
Args:
    logits, labels
Returns:
    returns scalar of loss


"""

def loss_function(logits, labels):
    softmax_score = F.softmax(logits, dim = -1)
    loss = F.cross_entropy(softmax_score, labels)
    return loss.item()
    
    

        





    # def __init__(self, margin=1.0):
    #     super(CustomLossFunction, self).__init__()
    #     self.margin = margin
    #     self.model = SentenceTransformer('distilbert-base-uncased')
    #     self.training_examples = gptdatagenerator.generate_qa()  # Assuming gptdatagenerator generates input examples
    #     self.train_dataloader = DataLoader(self.training_examples, shuffle=True, batch_size=16) 

    # def forward(self, predictions, targets):
    #     pairwise_distances = self.compute_pairwise_distances(predictions)
    #     loss = self.pairwise_ranking_loss(pairwise_distances, targets)
    #     return loss

    # def compute_pairwise_distances(self, predictions):
    #     # Compute pairwise distances (e.g., cosine similarity) between predictions
    #     embeddings = self.model.encode(predictions)  # Assuming 'predictions' are texts
    #     pairwise_distances = 1 - torch.cosine_similarity(embeddings.unsqueeze(1), embeddings.unsqueeze(2), dim=-1)
    #     return pairwise_distances

    # def pairwise_ranking_loss(self, pairwise_distances, targets):
    #     # Compute pairwise ranking loss between similarities and predicted
    #     positive_pairs = pairwise_distances[targets == 1] 
    #     negative_pairs = pairwise_distances[targets == 0]
    #     loss = torch.mean(torch.clamp(self.margin + positive_pairs - negative_pairs, min=0))
    #     return loss


# Assuming you have a defined model, dataloader, and other components
embedder = Embedder("microsoft/codebert-base")
transformer = Transformer("codellama/CodeLlama-7b-Instruct-hf")
loss_function = lossFunction()
optimizer = torch.optim.AdamW(embedder.model.parameters(), lr=5e-5)

for epoch in range(num_epochs):
    embedder.model.train()  # Set the model to training mode
    for batch in train_dataloader:
        # Forward pass
        embeddings = embedder.train(batch['texts'])
        logits = transformer.predict(batch['texts'], batch['context'])

        # Compute loss
        loss = loss_function(logits, embeddings)  # Ensure this aligns with what you're trying to achieve
        
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()