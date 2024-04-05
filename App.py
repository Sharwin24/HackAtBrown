import dash
from create_layout import create_layout
from visualziation_callbacks import Visualization_callback



app = dash.Dash(__name__, suppress_callback_exceptions=True)
layout = create_layout()

app.layout = layout
Visualization_callback(app)



if __name__ == '__main__':
    app.run_server(debug=False)
