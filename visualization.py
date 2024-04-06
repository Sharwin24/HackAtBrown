import plotly.express as px
from napkin_graph import CodeBase, CodeGraph
"""
The structure of graph_dict is as follows:
dict[File, list[dict[Class, list[Function]]]]
File, Class, and Function are Component objects
There are no repeated names for files, classes, functions
{
    File1: [
        {
            Class1: [
                Function1,
                Function2
            ]
        }
    ],
}
"""

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


class KnowledgeGraphVisualizer():

    def __init__(self) -> None:
        self.names_list = []
        self.parents_list = []
        self.graph_dict = None
        self.lonelyFunctions = {}
        self.repo_name = None

    def __repr__(self) -> str:
        length = len(self.names_list)
        print(f"Visualization of plotly treemap:")
        for i in range(length):
            print(f'{self.names_list[i]} -> {self.parents_list[i]}')

    def upload_repository(self, repo_name: str, repo_dir: str, repo_link: str, skip_cloning: bool = False) -> None:
        ''' Uploads the repository to be visualized and creates the graph_dict.
            Args:
                repo_name (str): The name of the repository. Internal name for the codebase.
                repo_dir (str): The directory where the repository will be cloned to.
                repo_link (str): The https link to the repository for running git clone command. Should end with .git
                skip_cloning (bool): If True, the repository will not be cloned again and the codebase will be created from the existing directory.
        '''
        self.repo_name = repo_name
        cb = CodeBase(repo_name, repo_dir, repo_link, skip_cloning)
        cg = CodeGraph(cb)
        cg.set_debug(False)
        cg.populate_graph()
        cg.populate_func_call_edges()
        cg.reindex_nodes()
        # print(cg)
        visual_cg = VisualCodeGraph(cg)
        self.graph_dict = visual_cg.get_graph_dict()
        self.lonelyFunctions = visual_cg.get_lonely_functions()

    def format_raw_text(self, raw_text: str) -> str:
        ''' Formats the raw text to replace newlines with <br> tags.
            Args:
                raw_text (str): The raw text to be formatted.
            Returns:
                str: The formatted raw text.
        '''
        raw_text = raw_text.replace('\n', '<br>')
        return raw_text.strip()

    def generate_lists(self):
        ''' Populate the names_list and parents_list attributes based on the graph_dict.
            Iterates through the graph_dict, extracting file names, class names, function names, 
            and raw text to populate names_list and their corresponding parent relationships in parents_list.
        '''
        for file, classes in self.graph_dict.items():
            if file.name not in self.names_list:
                self.names_list.append(file.name)
                self.parents_list.append(self.repo_name)
            for classes_dict in classes:
                for class_obj, functions in classes_dict.items():
                    if class_obj.name not in self.names_list:
                        self.names_list.append(class_obj.name)
                        self.parents_list.append(file.name)
                    for function in functions:
                        if function.name not in self.names_list:
                            self.names_list.append(function.name)
                            self.parents_list.append(class_obj.name)
                            formatted_raw = self.format_raw_text(function.raw)
                            self.names_list.append(formatted_raw)
                            self.parents_list.append(function.name)
        # # # Add lonely functions to the treemap, the file should already exist in the treemap
        # for func, f in self.lonelyFunctions.items():
        #     if func.name not in self.names_list:
        #         self.names_list.append(func.name)
        #         self.parents_list.append(f.name)
        #         formatted_raw = self.format_raw_text(func.raw)
        #         self.names_list.append(formatted_raw)
        #         self.parents_list.append(func.name)

    def build_graph(self):
        '''
        Builds the treemap using the names_list and parents_list
        '''
        # Print the duplicates if there are any in either the names_list or parents_list
        # if len(self.names_list) != len(set(self.names_list)):
        #     print("Duplicate names in names_list")
        #     # print the duplicate names
        #     for name in self.names_list:
        #         if self.names_list.count(name) > 1:
        #             print(name)

        fig = px.treemap(
            names=self.names_list,
            parents=self.parents_list
        )
        fig.update_traces(
            root_color="lightgrey",
            marker=dict(cornerradius=5),
            textfont=dict(size=24)
        )
        fig.update_layout(
            margin=dict(t=5, l=5, r=5, b=5),
            font=dict(size=24)
        )
        # fig.show()
        return fig
