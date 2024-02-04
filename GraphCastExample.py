import numpy as np
from model import Embedder
import torch
from transformers import AutoTokenizer, AutoModel
import os
import json

#embedding repo per file

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Move the model to the selected device

# Initialize the embedder
embedder = Embedder("microsoft/codebert-base")

# Directory containing .py files
# directory_path = '/home/iyer.ris/graphcast/graphcast'
directory_path = 'graphcast/graphcast'

# Directory to store the embeddings
embeddings_path = 'GraphCastEmbeddings/'

# Create the directory if it doesn't exist
os.makedirs(embeddings_path, exist_ok=True)

# Loop through the JSON and get the embeddings

# Read example_codebase.json
with open('graphcast.json', 'r', encoding='utf-8') as file:
    nodeIdToRawText = json.load(file)
    
embeddings_list = []

for nodeId, rawText in nodeIdToRawText.items():
    # Ensure the rawText is a string
    if isinstance(rawText, str):
        # Get embeddings for the raw text
        embeddings = embedder.embed(rawText)
        
        # Move embeddings to CPU if you plan to use numpy or save in a non-GPU format
        embeddings = embeddings.to('cpu')

        # Collect embeddings
        embeddings_list.append(embeddings)
embeddingMatrix = torch.vstack(embeddings_list)

    
    # Define the path to save the embeddings
    # embeddings_file_path = os.path.join(embeddings_path, nodeId + '.pt')
    
    # Save the embeddings
torch.save(embeddingMatrix, 'vectordb.pt')

print(embeddingMatrix.shape)

print('Embeddings are saved successfully.')