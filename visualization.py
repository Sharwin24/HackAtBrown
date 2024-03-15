import plotly.express as px
from napkin_graph import CodeBase, CodeGraph, VisualCodeGraph

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


class Visualization_Graph():

    def __init__(self) -> None:
        self.names_list = []
        self.parents_list = []
        self.graph_dict = None

    def __repr__(self) -> str:
        length = len(self.names_list)
        print(f"Visualization of plotly treemap:")
        for i in range(length):
            print(f'{self.names_list[i]} -> {self.parents_list[i]}')

    def upload_repository(self, repo_name: str, repo_dir: str, repo_link: str, skip_cloning: bool = True) -> None:
        ''' Uploads the repository to be visualized and creates the graph_dict.
            Args:
                repo_name (str): The name of the repository. Internal name for the codebase.
                repo_dir (str): The directory where the repository will be cloned to.
                repo_link (str): The https link to the repository for running git clone command. Should end with .git
                skip_cloning (bool): If True, the repository will not be cloned again and the codebase will be created from the existing directory.
        '''
        cb = CodeBase(repo_name, repo_dir, repo_link, skip_cloning)
        cg = CodeGraph(cb)
        cg.populate_graph()
        cg.populate_func_call_edges()
        cg.reindex_nodes()
        visual_cg = VisualCodeGraph(cg)
        self.graph_dict = visual_cg.get_graph_dict()
        # print(f"Graph Dictionary:\n{graph_dict}")

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
                self.parents_list.append('')
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

    def build_graph(self):
        '''
        Builds the treemap using the names_list and parents_list
        '''
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
        fig.show()


visualization_graph = Visualization_Graph()
# visualization_graph.upload_repository(
#     repo_name="GraphCast", repo_dir="graphcast", repo_link="https://github.com/google-deepmind/graphcast.git", skip_cloning=True)
visualization_graph.upload_repository(
    repo_name="IMU_RobotArm_Controller", repo_dir="imu-robotarm-control", repo_link="https://github.com/Sharwin24/IMU-RobotArm-Control.git", skip_cloning=False)
visualization_graph.generate_lists()
visualization_graph.build_graph()
# print(visualization_graph)
