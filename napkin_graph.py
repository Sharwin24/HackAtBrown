"""
@summary: Generates the graph for a codebase with nodes
					representing files and edges representing the dependencies/imports
"""

import os
import sys

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
		return self.dependencies[file]
	
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
						dependency = line.split(" ")[1]
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
	""" The graph for a codebase with nodes representing files and edges representing the dependencies/imports
			Pass a complete CodeBase object to the constructor to generate the graph
	"""

	def __init__(self, codebase: CodeBase) -> None:
		self.codebase = codebase
		self.nodes = codebase.get_files()
		self.edges = [] # tuple[File, File]
  
	def populate(self) -> None:
		""" Populates the graph with nodes and edges
		"""
		for file in self.nodes:
			dependencies = self.codebase.get_dependencies(file)
			for dependency in dependencies:
				self.add_edge(file, dependency)


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

# Save examples to a JSON
import json
with open('example_codebase.json', 'w') as f:
	json.dump(examples, f, default=lambda o: o.__dict__, indent=2)
