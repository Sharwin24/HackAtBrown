import plotly.express as px
from napkin_graph import *

# codebase = CodeBase()
# codegraph = CodeGraph()
# visual_cg = VisualCodeGraph(codegraph)
# graph_dict = visual_cg.get_graph_dict()



#This is an example graph_dict for testing puproses, replace with visual_cg.get_graph_dict()
#Make sure that there are no repeated names for files, classes, and functions
graph_dict= {
    'file1.py': [{'Class1': ['Function1', 'Function2']}, {'Class2': ['Function3', 'Function4']}],
    'file2.py': [{'Class2.1': ['Function5', 'Function6']}, {'Class2.2': ['Function7', 'Function8']}],
    'file3.py': [{'Class3.1': ['Function9', 'Function10']}, {'Class3.2': ['Function11', 'Function12']}]
}

class Visualization_Graph():
    
    graph_dict = graph_dict

    def __init__(self) -> None:
        self.names_list = []
        self.parents_list = []

    def generate_lists(self):
        ''' Populate the names_list and parents_list attributes based on the graph_dict.
            Iterates through the graph_dict, extracting file names, class names, and function names
            to populate names_list and their corresponding parent relationships in parents_list.
        '''
        for file, classes in self.graph_dict.items():
            self.names_list.append(file)
            self.parents_list.append('')
            for classes_dict in classes:
                for class_name, functions in classes_dict.items():
                    self.names_list.append(class_name)
                    self.parents_list.append(file)
                    # print(class_name)
                    for function in functions:
                        self.names_list.append(function)
                        self.parents_list.append(class_name)
                        # print(function)
                        pass


    def build_graph(self):
        '''
        Builds the treemap using the names_list and parents_list
        '''
        fig = px.treemap(

            names= self.names_list,
            parents=self.parents_list
        )
        fig.update_traces(root_color="lightgrey")
        fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
        fig.show()

visualization_graph = Visualization_Graph()
visualization_graph.generate_lists()
visualization_graph.build_graph()
# print(visualization_graph.names_list)
# print(visualization_graph.parents_list)
