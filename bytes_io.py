import base64
import io
import cv2
import numpy as np

from dash import *

app = dash.Dash(__name__)

src = 'assets/mustang.jpg'
img = cv2.imread(src)


img_buffer = io.BytesIO()
# cv2.imwrite(img_buffer, img)

encoded_image = cv2.imencode('.jpg', img)[1]
img_buffer.write(np.array(encoded_image).tobytes())

img_buffer.seek(0)
# data = img_buffer.read()

str_equivalent_image = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
img_tag = "<img src='data:image/jpg;base64,".format(str_equivalent_image)


app.layout = html.Div([
    html.Div([
            html.Img(
                id="video-player1",
                src=img_tag
            )
        ])
])


if __name__ == '__main__':

    app.run_server(debug=True)
