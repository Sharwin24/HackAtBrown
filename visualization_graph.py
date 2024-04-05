

import plotly.express as px
from visualization import KnowledgeGraphVisualizer


# Define a separate function to build the graph
def build_graph(repo_name, repo_link):
    '''
        Builds a treemap graph based on the provided repository name and link.

    Parameters:
    - repo_name (str): The name of the repository.
    - repo_link (str): The link to the repository.

    Returns:
    - plotly.graph_objs.Figure: The treemap graph figure.

    '''
    if repo_name and repo_link:
        visualizer = KnowledgeGraphVisualizer()
        visualizer.upload_repository(
            repo_name=repo_name,
            repo_dir=repo_name + "_dir",
            repo_link=repo_link,
            skip_cloning=False
        )
        visualizer.generate_lists()

        fig = px.treemap(
            names=visualizer.names_list,
            parents=visualizer.parents_list
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


# import plotly.express as px
# from visualization import KnowledgeGraphVisualizer


# # Define a separate function to build the graph
# def build_graph(repo_name, repo_link):

#     '''
#         Builds a treemap graph based on the provided repository name and link.

#     Parameters:
#     - repo_name (str): The name of the repository.
#     - repo_link (str): The link to the repository.

#     Returns:
#     - plotly.graph_objs.Figure: The treemap graph figure.

#     '''
#     visualizer = KnowledgeGraphVisualizer()
#     visualizer.upload_repository(
#         repo_name=repo_name,
#         repo_dir=repo_name, #may have to comeback and change it
#         repo_link=repo_link,
#         skip_cloning=False
# )
#     visualizer.generate_lists()

#     fig = px.treemap(
#         names=visualizer.names_list,
#         parents=visualizer.parents_list
#     )
#     fig.update_traces(
#         root_color="lightgrey",
#         marker=dict(cornerradius=5),
#         textfont=dict(size=24)
#     )
#     fig.update_layout(
#         margin=dict(t=5, l=5, r=5, b=5),
#         font=dict(size=24)
#     )
#     # fig.show()
#     # print(repo_name)
#     return fig

# # Call the build_graph function
# # graph_instance = Graph()
# # graph_instance.build_graph("IMU_RobotArm_Controller", "https://github.com/Sharwin24/IMU-RobotArm-Control.git")
