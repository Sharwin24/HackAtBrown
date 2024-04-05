import dash
from create_layout import create_layout
from visualziation_callbacks import Visualization_callback


app = dash.Dash(__name__, suppress_callback_exceptions=True)
layout = create_layout()

app.layout = layout
Visualization_callback(app)


if __name__ == '__main__':
    app.run_server(debug=False)

# Example Repositories:
# https://github.com/google-research/bert.git
# https://github.com/Sharwin24/IMU-RobotArm-Control.git
# https://github.com/google-deepmind/graphcast.git
