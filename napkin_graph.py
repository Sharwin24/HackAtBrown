"""
@summary: Generates the graph for a codebase with nodes
					representing files and edges representing the dependencies/imports
"""

import os
import sys

class File:
	""" File is a representation of a file in a codebase
	"""
	def __init__(self, name: str, extension: str) -> None:
		self.name = name
		self.extension = extension
  
	def __str__(self) -> str:
		return f"{self.name}.{self.extension}"

class CodeBase:
	""" CodeBase is a representation of the codebase of a project, containing all files and their dependencies
	"""
	def __init__(self) -> None:
		self.files = [] # list[File]
		self.dependencies = {} # {File: list[str]}
  
	def add_file(self, file: File or str, dependencies: 'list[File]' or 'list[str]') -> None:
		""" Adds a file to the codebase with its dependencies
  
		Args:
				file (str): The file to be added (including file extension)
				dependencies ('list[str]'): The list of dependencies of the file
		"""
		self.files.append(file)
		self.dependencies[file] = dependencies
  
	def remove_file(self, file: File or str) -> None:
		""" Removes a file from the codebase

		Args:
				file (str): The file to be removed (including file extension)
		"""
		self.files.remove(file)
  
	def add_dependency(self, file: File or str, dependency: File or str) -> None:
		""" Add a dependency to a file

		Args:
				file (str): The file to which the dependency is to be added
				dependency (str): The dependency to be added
		"""
		self.dependencies[file].append(dependency)
  
	def remove_dependency(self, file: File or str, dependency: File or str) -> None:
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

	def get_dependencies(self, file: File or str) -> 'list[str]':
		""" Get the dependencies of a file

		Returns:
				'list[str]': The list of dependencies of the file
		"""
		return self.dependencies[file]

class CodeGraph:
	""" The graph for a codebase with nodes representing files and edges representing the dependencies/imports
	"""

	def __init__(self, codebase: CodeBase) -> None:
		self.codebase = codebase
		self.nodes = codebase.get_files()
		self.edges = []
  
	def add_edge(self, file1: File or str, file2: File or str) -> None:
		""" Adds an edge between two files

		Args:
				file1 (str): The first file
				file2 (str): The second file
		"""
		self.edges.append((file1, file2))
  
	def remove_edge(self, file1: File or str, file2: File or str) -> None:
		""" Removes an edge between two files

		Args:
				file1 (str): The first file
				file2 (str): The second file
		"""
		self.edges.remove((file1, file2))
