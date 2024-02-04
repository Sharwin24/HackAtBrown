import numpy as np
from model import Embedder
import torch
from transformers import AutoTokenizer, AutoModel
import os

#embedding repo per file


# Initialize the embedder
embedder = Embedder("microsoft/codebert-base")

# Directory containing .py files
directory_path = '/home/iyer.ris/graphcast/graphcast'

# Directory to store the embeddings
embeddings_path = '/home/iyer.ris/HackAtBrown/GraphCastEmbeddings'

# Create the directory if it doesn't exist
os.makedirs(embeddings_path, exist_ok=True)

# Loop through each file in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.py'):
        file_path = os.path.join(directory_path, filename)
        
        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
        
        # Get embeddings for the file content
        embeddings = embedder.embed(file_content)
        
        # Define the path to save the embeddings
        embeddings_file_path = os.path.join(embeddings_path, filename + '.pt')
        
        # Save the embeddings
        torch.save(embeddings, embeddings_file_path)

print('Embeddings are saved successfully.')