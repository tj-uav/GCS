import json
import time
import threading
import socket
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import cv2
import numpy as np

TCP_IP = '127.0.0.1'  # Need to change to IP of comms computer
TCP_PORT = 5005
BUFFER_SIZE = 1024  # Can make this lower if we need speed

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.connect((TCP_IP, TCP_PORT))
global image_num
image_num = 0

def save_image(image_string):
    global image_num
#    image_string = image_bytes.decode('utf-8')
    nparr = np.fromstring(image_string, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite("assets/LiveImage" + str(image_num) + ".png", img)
    image_num += 1

def sock_recv():
    while True:
        temp = sock.recv(1000000)
        save_image(temp)

sock_thread = threading.Thread(target=sock_recv)
sock_thread.start()

app = Flask("__name__", static_folder="assets")

# Prevent CORS errors
CORS(app)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    print('hi')
    return 'hi'
if __name__ == "__main__":
    app.run()
