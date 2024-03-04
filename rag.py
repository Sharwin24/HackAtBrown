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
		print(f"{self.similarities}")
		self.walkThreshold = 0.9
		self.augmentationNodesById = []
		self.indexToNodeID, self.nodeIDToIndex = self.knowledgeGraph.create_index_to_json_dict()

	def getMostSimilarNode(self) -> int:
		""" Returns the most similar node by id to the similarities vector
		"""
		print(f"Starting Node {torch.topk(self.similarities,5)}")
		
		return torch.argmax(self.similarities).item()

	def reset_augmentation(self) -> None:
		self.augmentationNodesById = []

	def graph_walk(self, start_node_id: int):
		""" Walks the graph to find the most similar nodes
		
		Args:
			start_node_id (int): The starting node for the graph walk [node_id]
		"""
		starting_node = self.knowledgeGraph.get_node_by_id(start_node_id)
		# Base case
		if self.similarities[self.nodeIDToIndex[start_node_id]] < self.walkThreshold:
			if len(self.augmentationNodesById) == 0:
				self.augmentationNodesById.append(starting_node)
			return self.augmentationNodesById
		# Get neighbors and find the most similar one by cosine similarity
		self.augmentationNodesById.append(starting_node)
		neighbors = self.knowledgeGraph.find_connected_nodes(starting_node)
		neighborsById = []
		for node in neighbors:
			if node != None:
				try:
					neighborsById.append(self.nodeIDToIndex[node.id])
				except KeyError:
					continue
		scores = self.similarities[neighborsById]
		maxScore = torch.max(scores)
		newStartNode = 0
		for i, _ in enumerate(scores):
			if self.similarities[i] == maxScore:
				newStartNode = self.indexToNodeID[i]
				break
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
# graphcastGraph.create_id_to_raw_json()
print(graphcastGraph)

# Usage Example
prompt = "what does the function _build_update_fns_for_node_types do"
RAG = RetrievalAugmentedGeneration(prompt, graphcastGraph)
# print(RAG.getMostSimilarNode())
# print(RAG.graph_walk(RAG.getMostSimilarNode()))