import json
import time
import threading
import socket
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import cv2
import numpy as np
import requests

global x
x = 1
TCP_IP = '127.0.0.1'  # Need to change to IP of comms computer
TCP_PORT = 5005
BUFFER_SIZE = 1024  # Can make this lower if we need speed

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.connect((TCP_IP, TCP_PORT))
global image_num
image_num = 20

def save_image(img):
    global image_num
#    image_string = image_bytes.decode('utf-8')
#    nparr = np.fromstring(image_string, np.uint8)
#    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#    cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
#    print(image_num)
    cv2.imwrite("assets/img/image_" + str(image_num) + ".png", img)
    image_num += 1

def video_thread():
    global x
    cap = cv2.VideoCapture(0)
    time.sleep(1)
    while True:
    	ret, frame = cap.read()
    	save_image(frame)
    	time.sleep(1)
    	stuff = 5/x
    cap.release()
    cv2.destroyAllWindows()

#vid_thread = threading.Thread(target=video_thread)
#vid_thread.start()

app = Flask("__name__", static_folder="assets")

# Prevent CORS errors
CORS(app)
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/receiver')
def receiver():
	data = request.get_json()
	print(data)

@app.route("/data")
def data():
    global image_num
    return jsonify({"highest":image_num})

if __name__ == "__main__":
    app.run()
    x = 0
