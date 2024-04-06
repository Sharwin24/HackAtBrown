import plotly.express as px
import dash
import dash_mantine_components as dmc
from dash import html, dcc
from dash.dependencies import Input, Output
from visualization import KnowledgeGraphVisualizer


def create_layout():
    visualization_layout = html.Div(children=[
        html.H1(children='Knowledge Graph Treemap Visualization', style={
                'textAlign': 'center'}),
        html.Div(style={'display': 'flex', 'justifyContent': 'center'}, children=[
            dmc.SimpleGrid(
                cols=3,
                children=[
                    html.Div(dcc.Input(id="repo-name", type="text", placeholder="Github Repository Name",
                                       style={'width': '70vh', 'fontSize': '20px', 'margin-left': '200px'}, debounce=True)),
                    html.Div(dcc.Input(id="repo-link", type="text", placeholder="Github Repository Link",
                                       style={'width': '70vh', 'fontSize': '20px', 'margin-left': '200px'}, debounce=True)),
                    html.Div(html.Button(id='submit-button', type='submit', children='Submit',
                                         style={'width': '10vh', 'fontSize': '20px', 'margin-left': '200px'})),

                ])
        ]),
        html.Div([
            dcc.Graph(
                id='tree-map',
                style={'width': '100%', 'height': '100vh', 'marginTop': '25px'}
            ),
        ])
    ])
    return visualization_layout


def visualize_repo(repo_name, repo_link):
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
        fig = visualizer.build_graph()
        # fig.show()
        # print(repo_name)
        return fig


def visualization_callback(app):
    '''
    Callback function for generating a tree-map figure based on repository name and link inputs.

    Parameters:
    - app (Dash): The Dash application instance.

    Returns:
    - function: Callback function for Dash application.
    '''

    @app.callback(
        Output('tree-map', "figure"),
        Input('submit-button', 'n_clicks'),
        Input("repo-name", 'value'),
        Input('repo-link', 'value'),
        prevent_initial_call=True
    )
    def update_tree_map(n_clicks, repo_name, repo_link):
        if repo_name and repo_link:  # Ensure both inputs are provided
            return visualize_repo(repo_name, repo_link)
        else:
            # Return an empty figure or default figure if no inputs provided
            return {}
    return update_tree_map


app = dash.Dash(__name__, suppress_callback_exceptions=True)
layout = create_layout()

app.layout = layout
visualization_callback(app)

app.run_server(debug=False)

# Example Repositories:
# https://github.com/google-research/bert.git
# https://github.com/Sharwin24/IMU-RobotArm-Control.git
# https://github.com/google-deepmind/graphcast.git
