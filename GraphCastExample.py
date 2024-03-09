import numpy as np
from model import Embedder
import torch
from transformers import AutoTokenizer, AutoModel
import os
import json

class EmbeddingGenerator:
    
    def __init__(self, embeddingAgent: Embedder, directory_path: str, embeddings_file_path: str) -> None:
        """ Initializes the EmbeddingGenerator class with the Embedder
            and path to repository containing the .py files, and the path
            to the file where the embeddings file will be stored [.pt].

        Args:
            embeddingAgent (Embedder): An Embedder object built with a specific model
            directory_path (str): The path to the directory containing the .py files, or the repository
            embeddings_path (str): The name of the file where the embeddings will be stored as a .pt file
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")
        self.embeddingAgent = embeddingAgent
        # Create the directory if it doesn't exist
        os.makedirs(embeddings_path, exist_ok=True)
        self.directory_path = directory_path
    
    def generate_embeddings(self) -> None:
        """ Generates the embeddings for the .py files in the directory
        """
        with open('graphcast.json', 'r', encoding='utf-8') as file:
            nodeIdToRawText = json.load(file)
        embeddings_list = []
        # Loop through the JSON and get the embeddings
        for nodeId, rawText in nodeIdToRawText.items():
            # Ensure the rawText is a string
            if isinstance(rawText, str):
                # Get embeddings for the raw text
                embeddings = self.embeddingAgent.embed(rawText)
                
                # Move embeddings to CPU if you plan to use numpy or save in a non-GPU format
                embeddings = embeddings.to('cpu')
                
                 # Collect embeddings
                embeddings_list.append(embeddings)
        embeddingMatrix = torch.vstack(embeddings_list)
        # Define the path to save the embeddings
        # embeddings_file_path = os.path.join(embeddings_path, nodeId + '.pt')
        
        # Save the embeddings
        torch.save(embeddingMatrix, embeddings_file_path)
        
        print('Embeddings are saved successfully.')

# Initialize the embedder
embedder = Embedder("microsoft/codebert-base")

# Directory to store the embeddings
embeddings_path = 'GraphCastEmbeddings/'

    


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