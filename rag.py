import torch
import numpy as np
from model import Embedder
from napkin_graph import CodeGraph, CodeBase

class RetrievalAugmentedGeneration:
	""" Performs the RAG algorithm to obtain the most similar nodes to a given prompt
	"""
	def __init__(self, prompt: str, knowledgeGraph: CodeGraph) -> None:
		self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
		print(f"Using device: {self.device}")
		self.embeddingAgent = Embedder("microsoft/codebert-base")
		self.codebaseEmbeddingVector = torch.load("vectordb.pt").to(self.device)
		self.promptEmbedding = self.embeddingAgent.embed(prompt).to(self.device)
		self.knowledgeGraph = knowledgeGraph
		self.similarities = torch.cosine_similarity(self.codebaseEmbeddingVector, self.promptEmbedding).to(self.device)
		self.walkThreshold = 0.8
		self.augmentationNodesById = []

	def getMostSimilarNode(self) -> int:
		""" Returns the most similar node by id to the similarities vector
		"""
		return torch.argmax(self.similarities)

	def reset_augmentation(self) -> None:
		self.augmentationNodesById = []

	def graph_walk(self, start_node_id: int) -> None:
		""" Walks the graph to find the most similar nodes
		
		Args:
			start_node_id (int): The starting node for the graph walk [node_id]
		"""
		# Base case
		if self.similarities[start_node_id] < self.walkThreshold:
			return self.augmentationNodesById
		# Get neighbors and find the most similar one by cosine similarity
		starting_node = self.knowledgeGraph.get_node_by_id(start_node_id)
		neighbors = self.knowledgeGraph.find_connected_nodes(starting_node)
		neighborsById = [node.id for node in neighbors if node != None and node.id < self.knowledgeGraph.get_true_length()]
		scores = self.similarities[neighborsById]
		newStartNode = neighborsById[torch.argmax(scores)]
		self.augmentationNodesById.append(newStartNode)
		self.graph_walk(newStartNode)

# Create CodeBase Object
graphcastCodeBase = CodeBase("GraphCast", "graphcast", "https://github.com/google-deepmind/graphcast.git", skipCloning=True)

# Create CodeGraph Object and apply optimizations
graphcastGraph = CodeGraph(graphcastCodeBase)
graphcastGraph.populate_graph()
graphcastGraph.delete_small_nodes()
graphcastGraph.populate_func_call_edges()
graphcastGraph.remove_large_nodes()
graphcastGraph.delete_edges_to_non_existent_nodes()
graphcastGraph.reindex_graph()
# print(graphcastGraph)

# Usage Example
prompt = "How to read a file in Python?"
RAG = RetrievalAugmentedGeneration(prompt, graphcastGraph)
print(RAG.graph_walk(RAG.getMostSimilarNode()))