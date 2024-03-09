import numpy as np
from model import Embedder
import torch
from transformers import AutoTokenizer, AutoModel
import os
import json

class EmbeddingGenerator:
    
    def __init__(self, embeddingAgent: Embedder, knowledge_graph_json_path: str, embeddings_dir_path: str, embeddings_file_path: str) -> None:
        """ Initializes the EmbeddingGenerator class with the Embedder, path to CodeGraph JSON file,
            the path to the directory where the embeddings files will be stored,
            and the name of the file where the embeddings_matrix will be stored as a .pt file

        Args:
            embeddingAgent (Embedder): An Embedder object built with a specific model
            directory_path (str): The path to the CodeGraph JSON file
            embeddings_dir_path (str): The path to the directory where the embeddings files will be stored
            embeddings_file_path (str): The name of the file where the embeddings will be stored as a .pt file
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"EmbeddingGenerator using device: {self.device}")
        self.embeddingAgent = embeddingAgent
        self.json_path = knowledge_graph_json_path
        self.embeddings_dir_path = embeddings_dir_path
        self.embeddings_file_path = embeddings_file_path
    
    def generate_embeddings(self) -> None:
        """ Generates the embeddings for the .py files in the directory
        """
        with open(self.json_path, 'r', encoding='utf-8') as file:
            nodeIdToRawText = json.load(file)
        embeddings_list = []
        # Create the embeddings directory if it doesn't exist
        os.makedirs(self.embeddings_dir_path, exist_ok=True)
        # Loop through the JSON and get the embeddings from rawText
        for rawText in nodeIdToRawText.values():
            # Ensure the rawText is a string
            if isinstance(rawText, str):
                # Get embeddings for the raw text
                embeddings = self.embeddingAgent.embed(rawText)
                
                # Move embeddings to CPU if you plan to use numpy or save in a non-GPU format
                embeddings = embeddings.to('cpu')
                
                # Collect embeddings
                embeddings_list.append(embeddings)
        # Create the embeddings matrix by stacking the embeddings list
        embeddingMatrix = torch.vstack(embeddings_list)
        
        # Save the embeddings
        torch.save(embeddingMatrix, self.embeddings_file_path)
        
        print('Embeddings are saved successfully.')


# This file should only run once and generate the embeddings for the knowledge graph

# Initialize the embedder
embedder = Embedder("microsoft/codebert-base")

# Directory to store the embeddings
embeddings_dir_path = 'embeddings/'

# JSON file path
knowledge_graph_json_path = 'knowledge_graph.json'

# File to store the embeddings
embeddings_file_path = 'vectordb.pt'

# Initialize the EmbeddingGenerator
embeddingGenerator = EmbeddingGenerator(embedder, knowledge_graph_json_path, embeddings_dir_path, embeddings_file_path)

# Generate the embeddings
embeddingGenerator.generate_embeddings()