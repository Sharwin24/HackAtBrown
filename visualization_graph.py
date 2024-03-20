import plotly.express as px
from visualization import KnowledgeGraphVisualizer

class Graph():
    """
    A class for generating a treemap graph based on repository information.

    Attributes:
    - visualizer (KnowledgeGraphVisualizer): An instance of KnowledgeGraphVisualizer used for data visualization.

    Methods:
    - __init__(self): Initializes the Graph object.
    - build_graph(self, repo_name, repo_link): Builds a treemap graph based on the provided repository name and link.
    """
    def __init__(self) -> None:
        '''
        Intitializes KnowledgeGraphVisualizer object 
        '''
        self.visualizer = KnowledgeGraphVisualizer()

# Define a separate function to build the graph
    def build_graph(self, repo_name, repo_link):
        
        '''
         Builds a treemap graph based on the provided repository name and link.

        Parameters:
        - repo_name (str): The name of the repository.
        - repo_link (str): The link to the repository.

        Returns:
        - plotly.graph_objs.Figure: The treemap graph figure.
        
        '''
        self.visualizer.upload_repository(
            repo_name=repo_name,
            repo_dir=repo_name, #may have to comeback and change it 
            repo_link=repo_link,
            skip_cloning=False
    )
        self.visualizer.generate_lists(repo_name)

        fig = px.treemap(
            names=self.visualizer.names_list,
            parents=self.visualizer.parents_list
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
        # print(repo_name)
        return fig

# Call the build_graph function
# graph_instance = Graph()
# graph_instance.build_graph("IMU_RobotArm_Controller", "https://github.com/Sharwin24/IMU-RobotArm-Control.git")


    
