import threading

import dash
from dash import *
from PIL import Image
import cv2
from functools import partial

app = dash.Dash(__name__)

src = 'assets/GoogleChrom.mp4'
cap = cv2.VideoCapture(src)
is_playing = False


def read_image(cam):
    ret, frame = cam.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    scale_percent = 30  # )percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    pil_image = Image.fromarray(frame)

    return pil_image


frame = read_image(cap)


# def set_interval(func, interval, *args, **kvargs):
#     def func_wrapper():
#         set_interval(func, interval, *args, **kvargs)
#         func(*args, **kvargs)
#     timer = threading.Timer(interval, func_wrapper)
#     timer.start()
#     return timer


app.layout = html.Div([
    html.Div(
        html.H1("VideoPlayer")
    ),
    html.Div([
            html.Img(
                id="video-player1",
                src=frame
            ),
            html.Button("Start", id="start-button", n_clicks=0)
            ]),

    html.Div([
            # html.Img(
            #     id="video-player2",
            # ),
            html.Button("Stop", id="stop-button", n_clicks=0)
    ]),
    ])


@callback(
    Output('video-player1', 'src'),
    # Output('video-player2', 'src'),
    Input('start-button', 'n_clicks'),
    Input('stop-button', 'n_clicks'),
)
def update_video(start_clicks, stop_clicks):
    global frame
    triggered_button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    while triggered_button_id == 'start-button':
        print(start_clicks)
        frame = read_image(cap)
        return frame


if __name__ == '__main__':
    app.run_server(debug=True)
