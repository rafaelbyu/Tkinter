from dash import *
from dash.dependencies import Input, Output, State
import cv2
import base64
from PIL import Image
import numpy as np

video_path = 'assets/GoogleChrom.mp4'
video = cv2.VideoCapture(video_path)

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Store(id='live-update-text', data=0),
    html.Button('Start/Stop', id='start-button', n_clicks=0),
    html.Video(id='video-real', controls=True),
    html.Video(id='video-grey', controls=True),
    dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0)
])


def generate_thumbnail(image):
    # Переводит cv2 image в формат, пригодный для отображения в HTML
    ret, png = cv2.imencode('.png', image)
    return 'data:image/png;base64,{}'.format(base64.b64encode(png).decode('utf-8'))


@app.callback(Output('video-real', 'src'),
              [Input('interval-component', 'n_intervals')],
              [State('live-update-text', 'data'),
               State('start-button', 'n_clicks')])
def update_video(n, data, btn):
    if btn % 2:
        ret, frame = video.read()
        real = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        scale_percent = 30
        width = int(real.shape[1] * scale_percent / 100)
        height = int(real.shape[0] * scale_percent / 100)
        dim = (width, height)
        real_image = cv2.resize(real, dim, interpolation=cv2.INTER_AREA)
        # real_image = Image.fromarray(real_image)
        return generate_thumbnail(real_image)
    else:
        return None


@app.callback(Output('video-grey', 'src'),
              [Input('interval-component', 'n_intervals')],
              [State('live-update-text', 'data'),
               State('start-button', 'n_clicks')])
def update_video(n, data, btn):
    if btn % 2: # Если кнопка была нажата
        ret, frame = video.read()
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        scale_percent = 30
        width = int(grey.shape[1] * scale_percent / 100)
        height = int(grey.shape[0] * scale_percent / 100)
        dim = (width, height)
        grey = cv2.resize(grey, dim, interpolation=cv2.INTER_AREA)
        # grey = Image.fromarray(grey)
        return generate_thumbnail(grey)
    else:       # Пока кнопка не была нажата 
        return None


if __name__ == '__main__':
    app.run_server(debug=True)
