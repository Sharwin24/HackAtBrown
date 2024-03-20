from dash.dependencies import Input, Output
from visualization_graph import Graph

# class Visual_Callback():

def Visualization_callback(app): 
    '''
    Callback function for generating a tree-map figure based on repository name and link inputs.

    Parameters:
    - app (Dash): The Dash application instance.

    Returns:
    - function: Callback function for Dash application.
    '''
    graph = Graph()
    app.callback(
        Output('tree-map', "figure"),
        Input("repo-name", 'value'),       
        Input('repo-link', 'value'),
        prevent_initial_call=True
    )(graph.build_graph)

