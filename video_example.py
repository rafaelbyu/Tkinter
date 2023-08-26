from dash import *

app = dash.Dash(__name__)

src = 'assets/GoogleChrom.mp4'


app.layout = html.Div([
    dcc.Store(id='live-update-text', data=0),
    html.Button('Start/Stop', id='start-button', n_clicks=0),
    html.Video(id='video-real', controls=True),
    # html.Video(id='video-grey', controls=True),
    dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0)
])


@callback(
    Output('video-player1', 'autoPlay'),
    Output('video-player1', 'loop'),
    # Output('video-player2', 'autoPlay'),
    # Output('video-player2', 'loop'),
    # Output('video-player2', 'src'),
    Input('start-button', 'n_clicks'),
    # Input('start-button', 'n_clicks'),
    State('video-player1', 'autoPlay'),
    State('video-player1', 'loop'),
    # State('video-player2', 'autoPlay'),
    # State('video-player2', 'loop'),
)
def update_video(start_clicks, stop_clicks, auto_play1, loop1):
    auto_play1, loop1 = False
    if start_clicks > 0 and stop_clicks < 1:
        print(start_clicks)
        auto_play1, loop1 = True
        return auto_play1, loop1
    else:
        auto_play1, loop1 = False
        return auto_play1, loop1


if __name__ == '__main__':
    app.run_server(debug=True)
