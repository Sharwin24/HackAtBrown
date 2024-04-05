
from dash.dependencies import Input, Output
from visualization_graph import build_graph

# class Visual_Callback():

def Visualization_callback(app): 
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
            return build_graph(repo_name, repo_link)
        else:
            # Return an empty figure or default figure if no inputs provided
            return {}
    return update_tree_map

    


# from dash.dependencies import Input, Output
# from visualization_graph import build_graph

# # class Visual_Callback():

# def Visualization_callback(app): 
#     '''
#     Callback function for generating a tree-map figure based on repository name and link inputs.

#     Parameters:
#     - app (Dash): The Dash application instance.

#     Returns:
#     - function: Callback function for Dash application.
#     '''
#     # graph = Graph()
#     app.callback(
#         Output('tree-map', "figure"),
#         Input("repo-name", 'value'),       
#         Input('repo-link', 'value'),
#         prevent_initial_call=True
#     )(build_graph)

