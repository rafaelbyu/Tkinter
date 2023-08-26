import cv2
from flask import Flask, Response

app = Flask(__name__)

cap = cv2.VideoCapture('assets/GoogleChrom.mp4')


def gen():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # ret, jpeg_real = cv2.imencode('.jpg', frame)
        ret, jpeg_grey = cv2.imencode('.jpg', gray)
        # frame_real = jpeg_real.tobytes()
        frame_grey = jpeg_grey.tobytes()
        # yield (b'--frame\r\n'
        #        b'Content-Type: image/jpeg\r\n\r\n' + frame_real + b'\r\n')
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_grey + b'\r\n')
    cap.release()


@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
