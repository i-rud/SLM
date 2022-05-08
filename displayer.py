from flask import Flask, render_template, Response
from kombu import Connection
import cv2
import numpy as np
import sys
import time
import base64

app = Flask(__name__, static_folder='web/pages', template_folder='web/pages')
rabbit_url = 'amqp://guest:guest@localhost:5672//'

conn = Connection(rabbit_url)
simple_queue = conn.SimpleQueue('frames2')

def gen_frames():  
    while True:
        time.sleep(0.08)
        try:
            message = simple_queue.get_nowait()
            frame = message.payload
            frame = base64.b64decode(frame["frame"])
            message.ack()

            size = sys.getsizeof(frame) - 33
            np_array = np.frombuffer(frame, dtype=np.uint8)
            np_array = np_array.reshape((720, 1280, 3))
            
            _, frame = cv2.imencode('.JPEG', np_array)
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame.tostring() + b'\r\n')
        except Exception:
            print("exception")
    
    simple_queue.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
    #gen_frames()