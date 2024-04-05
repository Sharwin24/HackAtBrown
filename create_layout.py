from dash import html, dcc
import dash_mantine_components as dmc

def create_layout():
    visualization_layout = html.Div(children=[
        html.H1(children='Knowledge Graph Retrieval Treemap Visualization', style={'textAlign': 'center'}),
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

#  style={'width':'70vh', 'fontSize': '20px'}



# from dash import html
# from dash import dcc
# import dash_mantine_components as dmc

# # import dash_core_components as dcc
# # import dash_html_components as html


# def create_layout():
#     visualization_layout = html.Div(children=[
#         html.H1(children='Knowledge Graph Retrieval Treemap Visualization', style={
#                 'textAlign': 'center'}),
#         html.Div(style={'display': 'flex', 'justifyContent': 'center'}, children=[
#             dmc.SimpleGrid(
#                 cols=2,
#                 children=[
#                     html.Div(dcc.Input(id="repo-name", type="text", placeholder="Github Repository Name",
#                                        style={'width': '70vh', 'fontSize': '20px'}, debounce=True)),
#                     html.Div(dcc.Input(id="repo-link", type="text", placeholder="Github Repository Link",
#                                        style={'width': '70vh', 'fontSize': '20px'}, debounce=True))
#                 ])
#         ]),
#         html.Div([
#             dcc.Graph(
#                 id='tree-map',
#                 style={'width': '100%', 'height': '100vh', 'marginTop': '25px'}
#             ),
#         ])
#     ])
#     return visualization_layout
# #  style={'width':'70vh', 'fontSize': '20px'}
