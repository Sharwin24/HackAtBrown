"""
@summary: Generates the graph for a codebase with nodes
					representing files and edges representing the dependencies/imports
"""

import os
import sys
import ast
from dataclasses import dataclass
import itertools


class Component():
	""" The base class for all components of the codebase
	"""
  
	id_iter = itertools.count()
 
	def __init__(self, name: str, parent: 'Component', children: 'list[Component]', raw: str) -> None:
		self.name = name
		self.parent = parent
		self.children = children
		self.raw = raw
		self.id = next(self.id_iter)

	def __repr__(self) -> str:
		return f"{self.name}"

	def __hash__(self) -> int:
		return hash(self.id, self.name)

class File(Component):
	""" The class for a file in the codebase
	"""
 
	def __init__(self, name: str, parent: Component, children: 'list[Component]', raw: str, path: str, dependencies: 'list[File]') -> None:
		super().__init__(name, parent, children, raw)
		self.path = path
		self.dependencies = []
		try:
			self.raw = open(self.path, 'r').read()
		except UnicodeDecodeError:
			pass
  
	def __hash__(self) -> int:
		return hash(self.name)

class Class(Component):
	""" The class for a class in the codebase
	"""
	pass

class Function(Component):
	pass

class ComponentEdge:
	""" The class for an edge between two components in the codebase
	"""
 
	def __init__(self, from_component: Component, to_component: Component) -> None:
		self.from_component = from_component
		self.to_component = to_component

	def __repr__(self) -> str:
		return f"{self.from_component} -> {self.to_component}"

	def __hash__(self) -> int:
		return hash((self.from_component, self.to_component))

class CodeBase:
	""" CodeBase is a representation of the codebase of a project, containing all files and their dependencies
	"""
	def __init__(self, name: str, codebase_directory: str) -> None:
		self.name = name
		self.fileDictionary = {} # dict[str, File] - file name to file object
		# Add all files in the subdirectories of the codebase to the list of files
		for root, dirs, files in os.walk(codebase_directory):
			for file in files:
				if file.endswith('.py'):
					# Construct a Component object for the file
					f = File(name=file, path=os.path.join(root, file), parent=None, children=[], raw="", dependencies=[])
					self.fileDictionary[file] = f
		self.dependencies = {} # dict[file, list[dependency]]
	
	def get_files(self) -> 'list[File]':
		""" Get a list of files in the codebase

		Returns:
				'list[File]': The list of files in the codebase
		"""
		return self.fileDictionary.values()

	def get_dependencies(self, file: File) -> 'list[File]':
		""" Get the dependencies of a file

		Returns:
				'list[File]': The list of dependencies of the file
		"""
		try:
			return self.dependencies[file]
		except KeyError:
			return []
	
	# def populate_dependencies(self) -> None:
	# 	""" Populates the dependencies of the files in the codebase by reading the imports in the files
	# 	"""
	# 	for file in self.files:
	# 		dependencies = []
	# 		with open(file, 'r') as f:
	# 			try:
	# 				lines = f.readlines()
	# 			except UnicodeDecodeError:
	# 				print(f"Error reading file: {file}")
	# 				continue
	# 			for line in lines:
	# 				if line.startswith("import") or line.startswith("from"):
	# 					dependency = line.split(" ")[1].strip()
	# 					dependencies.append(dependency)
	# 		self.dependencies[file] = dependencies
	
	 
	# def populate_dependencies_ast(self) -> None:
	# 	""" Populates the dependencies of the files in the codebase using the ast module
	# 	"""
	# 	for file in self.files:
	# 		dependencies = []
	# 		with open(file, 'r') as f:
	# 			try:
	# 				tree = ast.parse(f.read())
	# 			except:
	# 				print(f"Error reading file: {file}")
	# 				continue
	# 			for node in ast.walk(tree):
	# 				if isinstance(node, ast.Import):
	# 					for alias in node.names:
	# 						dependencies.append(alias.name)
	# 				elif isinstance(node, ast.ImportFrom):
	# 					dependencies.append(node.module)
	# 		self.dependencies[file] = dependencies
	
	def __repr__(self) -> str:
		""" Prints the CodeBase with files and their dependencies

		Returns:
				str: The string representation of the CodeBase
		"""
		value = f"CodeBase: {self.name}\n"
		for file, file_obj in self.fileDictionary.items():
			try:
				value += f"{file} -> {self.dependencies[file]}\n"
			except KeyError:
				value += f"{file}\n"
		return value

class CodeGraph:
	""" The graph for a codebase with nodes representing components and edges representing the dependencies/imports
			Pass a complete CodeBase object to the constructor
	"""
	def __init__(self, codebase: CodeBase) -> None:
		self.codebase = codebase
		files = codebase.get_files()
		if not files or len(files) == 0:
			raise ValueError("The codebase is empty")
		self.fileSet = set(files)
		self.nodes = [] # List[Component]
		self.edges = [] # List[ComponentEdge]
  
	def __repr__(self) -> str:
		""" Prints the graph with nodes and edges
		"""
		value = f"CodeBase: {self.codebase.name} Graph with {len(self.nodes)} nodes and {len(self.edges)} edges\n"
		value += "\tNodes: \n"
		for node in self.nodes:
			value += f"{node} -> {self.find_connected_nodes(node)}\n"
		value += "\tEdges: \n"
		for edge in self.edges:
			value += f"{edge}\n"
		return value

	def get_node_by_id(self, id: int) -> Component:
		""" Gets a node by its id
		"""
		for node in self.nodes:
			if node.id == id:
				return node
		return None
	
	def add_node(self, node: Component) -> None:
		""" Adds a node to the graph
		"""
		self.nodes.append(node)
	
	def add_edge(self, edge: ComponentEdge) -> None:
		""" Adds an edge to the graph
		"""
		self.edges.append(edge)
  
	def find_connected_nodes(self, node: Component) -> 'list[Component]':
		""" Finds all nodes connected to a given node
		"""
		connected_nodes = []
		for edge in self.edges:
			if edge.from_component == node:
				connected_nodes.append(edge.to_component)
			elif edge.to_component == node:
				connected_nodes.append(edge.from_component)
		return connected_nodes
  
	def _dfs_build_deps(self, node: ast.AST, parent: Component = None) -> None:
		""" Recursively builds the dependencies of a component node
		"""
		if isinstance(node, ast.Import):
			for alias in node.names:
				if self.codebase.fileDictionary.__contains__(alias.name):
					dependency = self.codebase.fileDictionary[alias.name]
					self.add_edge(ComponentEdge(parent, dependency))
		elif isinstance(node, ast.ImportFrom):
			if self.codebase.fileDictionary.__contains__(node.module):
				dependency =self.codebase.fileDictionary[alias.name]
				self.add_edge(ComponentEdge(parent, dependency))
		elif isinstance(node, ast.ClassDef):
			current_component = Class(node.name, parent, [], ast.unparse(node))
			self.add_node(current_component)
			if parent:
				self.add_edge(ComponentEdge(parent, current_component))
			parent = current_component
		elif isinstance(node, ast.FunctionDef):
			current_component = Function(node.name, parent, [], ast.unparse(node))
			self.add_node(current_component)
			if parent:
				self.add_edge(ComponentEdge(parent, current_component))
			parent = current_component

		for child in ast.iter_child_nodes(node):
			self._dfs_build_deps(child, parent)
   
  
	def populate_graph(self) -> None:
		""" Populates the graph with component nodes and edges representing
		the files, classes, and functions in the codebase and their dependencies
		"""
		for file in self.codebase.get_files():
			self.add_node(file)
			tree = ast.parse(file.raw)
			self._dfs_build_deps(tree, file)
		

# Example usage

# Get the codebase
codebase_link = "https://github.com/google-deepmind/graphcast.git"
# Clear the example if it already exists
os.system("rm -rf example_codebase")
# Clone the codebase to a directory
os.system(f"git clone {codebase_link} example_codebase")
# Delete the .git directory and other unnecessary files
os.system("rm -rf example_codebase/.git")
os.system("rm -rf example_codebase/.gitignore")

examples = CodeBase("MyCodeBase", "small_repo")
# examples.populate_dependencies()
print(examples)

# Build a graph from the codebase
graph = CodeGraph(examples)
graph.populate_graph()
print(graph)

# print("populate_dependencies and populate_dependencies_ast are the same: ", all(set(examples.get_dependencies(file)) == set(examples_ast.get_dependencies(file)) for file in examples.get_files()))

# Save examples to a JSON
# import json
# with open('example_codebase.json', 'w') as f:
# 	json.dump(examples, f, default=lambda o: o.__dict__, indent=2)
