import base64
from dash import *
import numpy as np
from dash.dependencies import Output, Input
import cv2


last_frame = None


def generate_frame():
    global last_frame

    src = 'assets/GoogleChrom.mp4'
    cap = cv2.VideoCapture(src)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        last_frame = frame

        ret, buffer = cv2.imencode('.jpg', frame)

        frame_data = base64.b64encode(buffer).decode('utf-8')

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data.encode('utf-8') + b'\r\n')
    cap.release()
    return last_frame


app = Dash(__name__)


app.layout = html.Div([
    html.Img(id='video-stream'),
    dcc.Interval(
        id='interval-component',
        interval=1000,
        n_intervals=0
    )
])


@app.callback(
    Output('video-stream', 'src'),
    Input('interval-component', 'n_intervals')
)
def update_stream(n):
    return 'data:image/jpeg;base64,{}'.format(last_frame)


if __name__ == '__main__':
    app.run_server(debug=True)
