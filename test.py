import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, State, Input

if __name__ == '__main__':
    app = dash.Dash()

    app.layout = html.Div([
        dcc.Input(id='username', placeholder='Initial Value', type='text'),
        dcc.Input(id='email', placeholder='Initial Email', type='text'),
        html.Button(id='submit-button', type='submit', children='Submit'),
        html.Div(id='output_div')
    ])

    @app.callback(Output('output_div', 'children'),
                  [Input('submit-button', 'n_clicks')],
                  [State('username', 'value'),
                   State('email', 'value')]
                  )
    def update_output(clicks, username_value, email_value):
        if clicks is not None:
            return f'Username: {username_value}, Email: {email_value}'

    if __name__=='__main__':
        app.run_server(debug=False)
