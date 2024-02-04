"""
@summary: Generates the graph for a codebase with nodes
					representing files and edges representing the dependencies/imports
"""

import os
import sys
import ast
from dataclasses import dataclass

@dataclass
class Component:
	""" The base class for all components of the codebase
	"""
	id: int
	name: str
	parent: 'Component' = None
	children: 'list[Component]' = None
	raw: str = None

	def __repr__(self) -> str:
		return f"{self.name}"

	def __hash__(self) -> int:
		return hash(self.id, self.name)

@dataclass
class File(Component):
	""" The class for a file in the codebase
	"""
	path: str
	dependencies: 'list[File]' = None
	
	def __post_init__(self) -> None:
		self.dependencies = []
		self.raw = open(self.path, 'r').read()

@dataclass
class Class(Component):
	""" The class for a class in the codebase
	"""
	pass

@dataclass
class Function(Component):
	pass

@dataclass
class ComponentEdge:
	""" The class for an edge between two components in the codebase
	"""
	from_component: Component
	to_component: Component
	weight: int = 1

	def __repr__(self) -> str:
		return f"{self.from_component} -> {self.to_component}"

	def __hash__(self) -> int:
		return hash((self.from_component, self.to_component))

class CodeBase:
	""" CodeBase is a representation of the codebase of a project, containing all files and their dependencies
	"""
	def __init__(self, name: str, codebase_directory: str) -> None:
		self.name = name
		self.files = [] # list[str]
		# self.files = [f for f in os.listdir(codebase_directory) if f.endswith('.py')]
		# Add all files in the subdirectories of the codebase to the list of files
		for root, dirs, files in os.walk(codebase_directory):
			for file in files:
				if file.endswith('.py'):
					self.files.append(os.path.join(root, file))
		self.dependencies = {} # dict[file, list[dependency]]
  
	def add_file(self, file: str, dependencies: 'list[str]') -> None:
		""" Adds a file to the codebase with its dependencies
  
		Args:
				file (str): The file to be added (including file extension)
				dependencies ('list[str]'): The list of dependencies of the file
		"""
		self.files.append(file)
		self.dependencies[file] = dependencies
  
	def remove_file(self, file: str) -> None:
		""" Removes a file from the codebase

		Args:
				file (str): The file to be removed (including file extension)
		"""
		self.files.remove(file)
  
	def add_dependency(self, file: str, dependency: str) -> None:
		""" Add a dependency to a file

		Args:
				file (str): The file to which the dependency is to be added
				dependency (str): The dependency to be added
		"""
		self.dependencies[file].append(dependency)
  
	def remove_dependency(self, file: str, dependency: str) -> None:
		""" Remove a dependency from a file

		Args:
				file (str): The file from which the dependency is to be removed
				dependency (str): The dependency to be removed
		"""
		self.dependencies[file].remove(dependency)
  
	def remove_dependency(self, dependency: str) -> None:
		""" Remove a dependency from all files
  
		Args:
				dependency (str): The dependency to be removed
		"""
		for file in self.files:
			try:
				if dependency in self.dependencies[file]:
					self.dependencies[file].remove(dependency)
			except KeyError:
				continue
  
	def get_files(self) -> 'list[str]':
		""" Get a list of files in the codebase

		Returns:
				'list[str]': The list of files in the codebase
		"""
		return self.files

	def get_dependencies(self, file: str) -> 'list[str]':
		""" Get the dependencies of a file

		Returns:
				'list[str]': The list of dependencies of the file
		"""
		try:
			return self.dependencies[file]
		except KeyError:
			return []
	
	def populate_dependencies(self) -> None:
		""" Populates the dependencies of the files in the codebase by reading the imports in the files
		"""
		for file in self.files:
			dependencies = []
			with open(file, 'r') as f:
				try:
					lines = f.readlines()
				except UnicodeDecodeError:
					print(f"Error reading file: {file}")
					continue
				for line in lines:
					if line.startswith("import") or line.startswith("from"):
						dependency = line.split(" ")[1].strip()
						dependencies.append(dependency)
			self.dependencies[file] = dependencies
	
	def __repr__(self) -> str:
		""" Prints the CodeBase with files and their dependencies

		Returns:
				str: The string representation of the CodeBase
		"""
		value = f"CodeBase: {self.name}\n"
		for file in self.files:
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
		self.nodes = [] # List[Component]
		self.edges = [] # List[ComponentEdge]
  
	def add_node(self, node: Component) -> None:
		""" Adds a node to the graph
		"""
		self.nodes.append(node)
	
	def add_edge(self, edge: ComponentEdge) -> None:
		""" Adds an edge to the graph
		"""
		self.edges.append(edge)
  
	def _dfs_build_deps(self, node: ast.AST, parent: Component = None) -> None:
		""" Recursively builds the dependencies of a component node
		"""
		if isinstance(node, ast.Import):
			for alias in node.names:
				if alias.name in self.fileDictionary:
					dependency = self.fileDictionary[alias.name]
					self.add_edge(ComponentEdge(parent, dependency))
		elif isinstance(node, ast.ImportFrom):
			if alias.name in self.fileDictionary:
				dependency = self.fileDictionary[alias.name]
				self.add_edge(ComponentEdge(parent, dependency))
		elif isinstance(node, ast.ClassDef):
			current_component = Class(node.name, parent, [], ast.unparse(node))
			if parent:
				self.add_edge(ComponentEdge(parent, current_component))
			parent = current_component
		elif isinstance(node, ast.FunctionDef):
			current_component = Function(node.name, parent, [], ast.unparse(node))
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

examples = CodeBase("MyCodeBase", "example_codebase")
examples.populate_dependencies()
print(examples)

examples_ast = CodeBase("MyASTCodeBase", "example_codebase")
examples_ast.populate_dependencies_ast()
print(examples_ast)

print("populate_dependencies and populate_dependencies_ast are the same: ", all(set(examples.get_dependencies(file)) == set(examples_ast.get_dependencies(file)) for file in examples.get_files()))

# Save examples to a JSON
import json
with open('example_codebase.json', 'w') as f:
	json.dump(examples, f, default=lambda o: o.__dict__, indent=2)
