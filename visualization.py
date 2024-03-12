import plotly.express as px
from napkin_graph import CodeBase, CodeGraph, VisualCodeGraph

graphcastCodeBase = CodeBase(
    "GraphCast", "graphcast", "https://github.com/google-deepmind/graphcast.git", skipCloning=True)
graphcastGraph = CodeGraph(graphcastCodeBase)
graphcastGraph.set_debug(False)
graphcastGraph.populate_graph()
# graphcastGraph.delete_small_nodes()
graphcastGraph.populate_func_call_edges()
# graphcastGraph.remove_large_nodes()
graphcastGraph.reindex_nodes()
visualGraphCastCodeGraph = VisualCodeGraph(graphcastGraph)
graph_dict = visualGraphCastCodeGraph.get_graph_dict()

print(f"Graph Dictionary:\n{graph_dict}")

"""
The structure of graph_dict is as follows:
dict[File, list[dict[Class, list[Function]]]]
File, Class, and Function are Component objects
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

# This is an example graph_dict for testing puproses, replace with visual_cg.get_graph_dict()
# Make sure that there are no repeated names for files, classes, functions, and raw text

graph_dict = {
    'file1.py': [{'Class1': [{'Function1': "def raw_text"}, {'Function2': "def raw_text2"}]}],
    'file2.py': [{'Class3': [{'Function3': "def raw_text3"}, {'Function4': "def raw_text4"}, {'Function5': "def raw_text5"}]}],
    'file3.py': [{'Class4': [{'Function6': "def raw_text6"}, {'Function7': "def raw_text7"}, {'Function8': "def raw_text8"}]}]
}


class Visualization_Graph():

    def __init__(self) -> None:
        self.names_list = []
        self.parents_list = []
        self.graph_dict = graph_dict

    def generate_lists(self):
        ''' Populate the names_list and parents_list attributes based on the graph_dict.
            Iterates through the graph_dict, extracting file names, class names, function names, 
            and raw text to populate names_list and their corresponding parent relationships in parents_list.
        '''
        for file, classes in self.graph_dict.items():
            self.names_list.append(file)
            self.parents_list.append('')
            for classes_dict in classes:
                # print(classes_dict)
                # print(classes)
                for class_name, functions in classes_dict.items():
                    self.names_list.append(class_name)
                    # print(class_name)
                    self.parents_list.append(file)
                    # print(class_name)
                    for functions_dict in functions:
                        # print(functions_dict)
                        # print(functions)
                        for functions_names, raw_texts in functions_dict.items():
                            # print(functions_names)
                            # print(raw_texts)
                            self.names_list.append(functions_names)
                            self.parents_list.append(class_name)
                            self.names_list.append(raw_texts)
                            self.parents_list.append(functions_names)

    # This version shows without the raw text included
    # def generate_lists(self):
    #     ''' Populate the names_list and parents_list attributes based on the graph_dict.
    #         Iterates through the graph_dict, extracting file names, class names, and function names
    #         to populate names_list and their corresponding parent relationships in parents_list.
    #     '''
    #     for file, classes in self.graph_dict.items():
    #         self.names_list.append(file)
    #         self.parents_list.append('')
    #         for classes_dict in classes:
    #             for class_name, functions in classes_dict.items():
    #                 self.names_list.append(class_name)
    #                 self.parents_list.append(file)
    #                 # print(class_name)
    #                 for function in functions:
    #                     self.names_list.append(function)
    #                     self.parents_list.append(class_name)
    #                     # print(function)
    #                     pass

    def build_graph(self):
        '''
        Builds the treemap using the names_list and parents_list
        '''
        fig = px.treemap(

            names=self.names_list,
            parents=self.parents_list
        )
        fig.update_traces(root_color="lightgrey")
        fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
        fig.show()


visualization_graph = Visualization_Graph()
visualization_graph.generate_lists()
# visualization_graph.build_graph()
# print(visualization_graph.names_list)
# print(visualization_graph.parents_list)


# Exampple Treemap for testing purposes to help build children and parents list
# fig = px.treemap(


#     names= ['file1.py', 'Class1', 'Function1', 'raw_text1', 'Function2', 'raw_text2'],
#     parents=['', 'file1.py', 'Class1', 'Function1', 'Class1', 'Function2']

# )
# fig.update_traces(root_color="lightgrey")
# fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
# fig.show()

# names=  ['file1.py', 'Class1', 'Function1', 'Function2', 'def raw_text1', 'def raw_text2'],
# parents=['', 'file1.py', 'Class1', 'Class1', 'Function1', 'Function2']

# names=  ['file1.py', 'Class1', 'Function1', 'Function2', 'Class2', 'Function3', 'Function4', 'file2.py', 'Class2.1', 'Function5', 'Function6', 'Class2.2', 'Function7', 'Function8', 'file3.py', 'Class3.1', 'Function9', 'Function10', 'Class3.2', 'Function11', 'Function12']
# parents=['', 'file1.py', 'Class1', 'Class1', 'file1.py', 'Class2', 'Class2', '', 'file2.py', 'Class2.1', 'Class2.1', 'file2.py', 'Class2.2', 'Class2.2', '', 'file3.py', 'Class3.1', 'Class3.1', 'file3.py', 'Class3.2', 'Class3.2']
