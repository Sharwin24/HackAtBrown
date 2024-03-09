from napkin_graph import CodeBase, CodeGraph
from rag import RetrievalAugmentedGeneration

# Create CodeBase Object
graphcastCodeBase = CodeBase("GraphCast", "graphcast", "https://github.com/google-deepmind/graphcast.git", skipCloning=True)

# Create CodeGraph Object and apply optimizations
graphcastGraph = CodeGraph(graphcastCodeBase)
graphcastGraph.populate_graph()
graphcastGraph.delete_small_nodes()
graphcastGraph.populate_func_call_edges()
graphcastGraph.remove_large_nodes()
#graphcastGraph.delete_edges_to_non_existent_nodes()
graphcastGraph.reindex_nodes()
graphcastGraph.create_id_to_raw_json()
print(graphcastGraph)

# Usage Example
prompt = "what does the function _build_update_fns_for_node_types do"
RAG = RetrievalAugmentedGeneration(prompt, graphcastGraph)
# print(RAG.getMostSimilarNode())
# print(RAG.graph_walk(RAG.getMostSimilarNode()))

# [NotImplementedYet] Next Step: Take similar nodes from graph_walk and 
# paste raw text along with the prompt into LLM to generate a response

# [NotImplementedYet] Next Step: Synthetic training by comparing output to 
# GPT-4's response to the same prompt using the entire codebase as context

# [NotImplementedYet] Next Step: Bake all of this python code into a VSCode Extension
