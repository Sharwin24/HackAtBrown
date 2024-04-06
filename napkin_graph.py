"""
@summary: Generates the graph for a codebase with nodes
                    representing files and edges representing the dependencies/imports
"""

import os
import ast
import itertools
import json


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
        return f"{self.name} ({self.get_type()})"

    def __hash__(self) -> int:
        return hash((self.id))

    def __eq__(self, other: 'Component') -> bool:
        if not isinstance(other, Component):
            return False
        return self.id == other.id

    def get_type(self) -> str:
        """ Get the type of the component [File, Class, Function]
        """
        return self.__class__.__name__

    def is_file(self) -> bool:
        """ Check if the component is a file
        """
        return self.get_type() == "File"

    def is_class(self) -> bool:
        """ Check if the component is a class
        """
        return self.get_type() == "Class"

    def is_function(self) -> bool:
        """ Check if the component is a function
        """
        return self.get_type() == "Function"


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

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, ComponentEdge):
            return False
        return self.from_component == __value.from_component and self.to_component == __value.to_component


class CodeBase:
    """ CodeBase is a representation of the codebase of a project, containing all files and their dependencies
    """

    def __init__(self, name: str, codebase_directory: str, repoLink: str = "", skipCloning: bool = False) -> None:
        self.name = name
        self.fileDictionary = {}  # dict[str, File] - file name to file object
        # dict[str, Function] - function name to function object
        self.funcDictionary = {}
        # Make sure codebase_directory is in repos/
        if not codebase_directory.startswith("repos/"):
            codebase_directory = "repos/" + codebase_directory
        if repoLink != "" and not skipCloning:
            self.clone_repository(repoLink, codebase_directory)
        # Add all files in the subdirectories of the codebase to the list of files
        for root, dirs, files in os.walk(codebase_directory):
            for file in files:
                if file.endswith('.py'):  # Only python files
                    # Construct a Component object for the file
                    f = File(name=file, path=os.path.join(root, file),
                             parent=None, children=[], raw="", dependencies=[])
                    self.fileDictionary[file] = f
        self.dependencies = {}  # dict[file, list[dependency]]

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

    def clone_repository(self, link: str, cloneDir: str) -> None:
        """ Clones a repository from a link

        Args:
                link (str): The link to the repository
                cloneDir (str, optional): The directory to clone the repository to
        """
        # Skip cloning if the link or cloneDir is empty or if the link doesn't end with .git
        if link == "" or link == None or cloneDir == "" or cloneDir == None:
            return
        elif not link.endswith(".git"):
            # If the link doesn't end with .git, add it
            link += ".git"
        try:
            # Remove the existing codebase if it exists
            os.system("rm -rf " + cloneDir)
            # Clone the codebase to a directory
            os.system(f"git clone {link} " + cloneDir)
            # Delete the .git directory and other git files
            os.system("rm -rf " + cloneDir + "/.git")
            os.system("rm -rf " + cloneDir + "/.gitignore")
            os.system("rm -rf " + cloneDir + "/.gitattributes")
            os.system("rm -rf " + cloneDir + "/.gitmodules")
            os.system("rm -rf " + cloneDir + "/.gitkeep")
        except Exception as e:
            print(
                f"Error cloning repository from {link} to {cloneDir}\n Error: {e}")
        if os.path.exists(cloneDir):
            print(f"Cloned repository from {link} to {cloneDir}")

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
        # if not files or len(files) == 0:
        #     raise ValueError("fCodebase {codebase.name} has no files")
        self.nodes = []  # List[Component]
        self.edges = []  # List[ComponentEdge]
        self.debug = True

    def __repr__(self) -> str:
        """ Prints the graph with nodes and edges
        """
        value = f"CodeBase: {self.codebase.name} Graph with {len(self.nodes)} nodes and {len(self.edges)} edges\n"
        value += "\tNodes -> Edges: \n"
        for node in self.nodes:
            value += f"\t\t{node} -> {self.find_connected_nodes(node)}\n"
        return value

    def set_debug(self, debug: bool) -> None:
        """ Sets the debug mode for the graph,
            Debug mode prints additional information for each operation
        """
        self.debug = debug

    def get_node_by_id(self, id: int) -> Component:
        """ Gets a node by its id
        """
        for node in self.nodes:
            if node.id == id:
                return node
        return None

    def print_node_raw(self, id: int) -> None:
        """ Prints the raw code of a node
        """
        node = self.get_node_by_id(id)
        print(f"Node {id}, {node.name} raw:")
        if node:
            print(node.raw)
        else:
            print("Node not found")

    def add_node(self, node: Component) -> None:
        """ Adds a node to the graph
        """
        self.nodes.append(node)

    def add_edge(self, edge: ComponentEdge) -> None:
        """ Adds an edge to the graph
        """
        self.edges.append(edge)

    def create_adjacency_matrix(self) -> 'list[list[int]]':
        """ Creates an adjacency matrix for the graph using the node ids
        """
        max_id = max([node.id for node in self.nodes])
        id_range = range(max_id + 1)
        adjacency_matrix = [[0 for _ in id_range] for _ in id_range]
        for edge in self.edges:
            try:
                adjacency_matrix[edge.from_component.id][edge.to_component.id] = 1
                adjacency_matrix[edge.to_component.id][edge.from_component.id] = 1
            except IndexError:
                print(
                    f"Index out of range for edge {edge} with from_component ID {edge.from_component.id} and to_component ID {edge.to_component.id}")
        return adjacency_matrix

    def find_connected_nodes(self, node: Component) -> 'list[Component]':
        """ Finds all nodes connected to a given node
        """
        connected_nodes = []
        for edge in self.edges:
            if edge.from_component == node:
                connected_nodes.append(edge.to_component)
            elif edge.to_component == node:
                connected_nodes.append(edge.from_component)
        return list(set(connected_nodes))

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
                dependency = self.codebase.fileDictionary[alias.name]
                self.add_edge(ComponentEdge(parent, dependency))
        elif isinstance(node, ast.ClassDef):
            current_component = Class(node.name, parent, [], ast.unparse(node))
            self.codebase.funcDictionary[node.name] = current_component
            self.add_node(current_component)
            if parent:
                self.add_edge(ComponentEdge(parent, current_component))
            parent = current_component
        elif isinstance(node, ast.FunctionDef):
            current_component = Function(
                node.name, parent, [], ast.unparse(node))
            self.codebase.funcDictionary[node.name] = current_component
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
        if self.debug:
            print(f"Populating graph for {self.codebase.name}")
        for file in self.codebase.get_files():
            self.add_node(file)
            tree = ast.parse(file.raw)
            self._dfs_build_deps(tree, file)

    def _dfs_build_func_calls(self, node: ast.AST, parent: Component = None) -> None:
        """ Recursively builds the function call edges of the graph
        """
        if isinstance(node, ast.ClassDef) or isinstance(node, ast.FunctionDef):
            parent = self.codebase.funcDictionary[node.name]
        elif isinstance(node, ast.Call):
            funcname = ""
            if isinstance(node.func, ast.Name):
                funcname = node.func.id
            elif isinstance(node.func, ast.Attribute):
                funcname = node.func.attr
            if self.codebase.funcDictionary.__contains__(funcname):
                dependency = self.codebase.funcDictionary[funcname]
                self.add_edge(ComponentEdge(parent, dependency))

        for child in ast.iter_child_nodes(node):
            self._dfs_build_func_calls(child, parent)

    def populate_func_call_edges(self) -> None:
        """ Populates the graph with edges representing function calls
        """
        for file in self.codebase.get_files():
            if self.debug:
                print(f"Populating function call edges for {file.name}")
            tree = ast.parse(file.raw)
            self._dfs_build_func_calls(tree)

    def delete_small_nodes(self, threshold: int = 300) -> None:
        """ Deletes nodes with raw code less than threshold
        """
        for node in self.nodes:
            if len(node.raw) < threshold:
                self.nodes.remove(node)
                for edge in self.edges:
                    if edge.from_component == node or edge.to_component == node:
                        self.edges.remove(edge)

    def remove_large_nodes(self, threshold: int = 1800) -> None:
        """ Removes nodes with raw code more than threshold
        """
        for node in self.nodes:
            if len(node.raw) > threshold:
                connected_nodes = self.find_connected_nodes(node)
                # Connect connected_nodes to each other
                for i in range(len(connected_nodes)):
                    for j in range(i+1, len(connected_nodes)):
                        self.add_edge(ComponentEdge(
                            connected_nodes[i], connected_nodes[j]))
                self.nodes.remove(node)

    def remove_duplicate_edges(self) -> None:
        """ Removes duplicate edges from the graph
        """
        unique_edges = set()
        for edge in self.edges:
            if edge not in unique_edges and ComponentEdge(edge.to_component, edge.from_component) not in unique_edges:
                unique_edges.add(edge)
        self.edges = list(unique_edges)

    def create_id_to_raw(self) -> 'dict[int, str]':
        """ Creates a dictionary mapping node ids to their raw code
        """
        id_to_json, json_to_id = self.create_index_to_json_dict()
        id_to_raw = {}
        for node in self.nodes:
            id_to_raw[node.id] = node.raw
        return id_to_raw

    def create_id_to_raw_json(self, json_file_path: str) -> None:
        """ Saves the dictionary mapping node ids to their raw code to a JSON
        """
        # If the json file already exists, overwrite it
        if os.path.exists(json_file_path):
            os.remove(json_file_path)
        # Save examples to a JSON
        with open(json_file_path, 'w') as f:
            # Get id to raw dict
            # this should update the correct node values from creare_id_to_raw
            id_to_raw = self.create_id_to_raw()
            json.dump(id_to_raw, f, indent=4, sort_keys=True)

    def create_index_to_json_dict(self) -> 'tuple[dict[int, int], dict[int, int]]':
        """ Creates a dictionary mapping node ids to their index
        """
        id_to_json = {}  # Index to JSON Data (node id)
        json_to_id = {}  # JSON Data (node id) to Index
        for i, node in enumerate(self.nodes):
            id_to_json[i] = node.id
            json_to_id[node.id] = i
        return (id_to_json, json_to_id)

    def delete_edges_to_non_existent_nodes(self) -> None:
        """ Deletes edges to non-existent nodes
        """
        true_length = len(self.nodes)
        for edge in self.edges:
            if edge.from_component != None and edge.to_component != None:
                if edge.from_component.id >= true_length or edge.to_component.id >= true_length:
                    self.edges.remove(edge)

    def reindex_nodes(self):
        if self.debug:
            print("Reindexing nodes")
        new_id = 0
        for node in self.nodes:
            if self.debug:
                print(f"Reindexing node {node.id} to {new_id}")
            node.id = new_id
            new_id += 1


class VisualCodeGraph():
    """ Class for generating visualizations of the code graph
    """

    def __init__(self, codegraph: CodeGraph) -> None:
        self.codegraph = codegraph
        self.graph_dict = {}
        # LonelyFunctions are functions directly written into a class
        self.lonelyFunctions = {}
        self.graph_dict = self._create_graph_dict()

    def get_graph_dict(self, print: bool = False):
        if self.graph_dict:
            return self.graph_dict
        else:
            self.graph_dict = self._create_graph_dict()
        if print:
            print(f"Graph Dictionary:\n\t{self.graph_dict}")
        return self.graph_dict

    def get_lonely_functions(self):
        return self.lonelyFunctions

    def _create_graph_dict(self) -> 'dict[File, list[dict[Class, list[Function]]]]':
        """ Creates a dictionary representation of the graph
            where keys are files and values are a list of dictionaries
            representing the classes and their functions

            This function also populates self.lonelyFunctions

            Example Output:
            {
                'file1.py': [
                                {
                                    'Class1': ['Function1', 'Function2']
                                },
                                {
                                    'Class2': ['Function3', 'Function4']
                                }
                ]
            }
        Returns:
            dict[File, list[dict[Class, list[Function]]]]: The dictionary representation of the graph
        """
        graph_dict = {}
        nodes = self.codegraph.nodes
        for node in nodes:
            if node.is_file():
                file = node
                graph_dict[file] = []
                # Get the connected nodes
                connected_nodes = self.codegraph.find_connected_nodes(file)
                for connected_node in connected_nodes:
                    if connected_node.is_class():
                        class_dict = {}
                        class_dict[connected_node] = []
                        # Get the connected nodes
                        connected_nodes2 = self.codegraph.find_connected_nodes(
                            connected_node)
                        for connected_node2 in connected_nodes2:
                            if connected_node2 == None:
                                continue
                            elif connected_node2.is_function():
                                class_dict[connected_node].append(
                                    connected_node2)
                        graph_dict[file].append(class_dict)
                    elif connected_node.is_function():
                        print(
                            f"Found lonely Function {connected_node.name} -> File {file.name}")
                        self.lonelyFunctions[connected_node] = file
        return graph_dict
