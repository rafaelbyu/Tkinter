import dash
from dash import *
from PIL import Image
import cv2
import base64
import numpy as np
import threading


app = dash.Dash(__name__)


video_path = 'assets/GoogleChrom.mp4'
video = cv2.VideoCapture(video_path)
output = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, (640, 480))


def convert_to_gray(video_path):
    frames = []
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        scale_percent = 30
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        frame = Image.fromarray(frame)
        output.write(frame)
        frames.append(frame)
    output.release()
    video.release()
    return frames


def general_video_html(frames):

    for frame in frames:
        encoded_frame = cv2.imencode('.jpg', frame)[1]
        base64_frame = base64.b64encode(encoded_frame).decode('utf-8')
        # video_html.append(html.Img(src='data:image/jpg;base64,{}'.format(base64_frame)))
        return html.Img(src='data:image/jpg;base64,{}'.format(base64_frame))


def run_threads(frames):
        x = threading.Thread(target=general_video_html, args=(frames,))
        x.start()
        x.join()


gray_frames = convert_to_gray(video)
video_html = general_video_html(gray_frames)


app.layout = html.Div(children=[
    html.H1(children='Видео в серых тонах'),

    dcc.Loading(
        id='loading',
        type='circle',
        children=[html.Div(children=video_html,
                           id='video-container')
        ]
    ),

    html.Div(id='output'),

    html.Div([
        # html.Img(
        #     id="video-player2",
        # ),
        html.Button("Start", id="start-button", n_clicks=0)
    ]),
])


@app.callback(
    Output('video-container', 'children'),
    Input('start-button', 'n_clicks')
)
def update_video(start_clicks):
    global video
    if start_clicks:
        gray_frames = convert_to_gray(video)
        run_threads(gray_frames)


if __name__ == '__main__':
    app.run_server(debug=True)
