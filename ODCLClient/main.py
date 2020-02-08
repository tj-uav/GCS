import json
import time
import threading
import socket
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import cv2
import numpy as np
from collections import deque
import os

IMAGE_BASENAME = 'assets/img/'
IMAGE_ENDING = '.jpg'

BUFFER_SIZE = 1024000  # Can make this lower if we need speed

ODCL_SHAPECONV = {'CIRCLE' : 1, 'SEMICRICLE' : 2, 'QUARTER_CIRCLE' : 3, 'TRIANGLE' : 4, 'SQUARE' : 5, 'RECTANGLE' : 6, 'TRAPEZOID' : 7, 'PENTAGON' : 8, 'HEXAGON' : 9, 'HEPTAGON' : 10, 'OCTAGON' : 11, 'STAR' : 12, 'CROSS' : 13}
ODCL_COLORCONV = {'WHITE' : 1, 'BLACK' : 2, 'GRAY' : 3, 'RED' : 4, 'BLUE' : 5, 'GREEN' : 6, 'YELLOW' : 7, 'PURPLE' : 8, 'BROWN' : 9, 'ORANGE' : 10}
ODCL_ORIENTATIONCONV = {'N' : 1, 'NE' : 2, 'E' : 3, 'SE' : 4, 'S' : 5, 'SW' : 6, 'W' : 7, 'NW' : 8}

global app, image_num, MISSION_ID
app = Flask("__name__", static_folder="assets")
image_num = 1
MISSION_ID = 3


def main():
    global app
#    connect_server(server_url='127.0.0.1', port=5005)
    print('Connected to comms comp')
	# Prevent CORS errors
    CORS(app)
    app.run()

def connect_server(server_url, port):
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_url, port))
    recv_thread = threading.Thread(target=img_recv_loop)
    recv_thread.daemon = True
    recv_thread.start()


def img_recv_loop():
    global sock
    while True:
        buffer = int(sock.recv(1024).decode())
        data = sock.recv(BUFFER)
        npimg = np.fromstring(img, dtype=np.uint8)

        decimg=cv2.imdecode(data, cv2.IMREAD_COLOR)
        data = json.loads(data)
        img = data["image"]
        decimg=cv2.imdecode(data,1)
        cv2.imwrite()

def decode_img():
    pass

def submit_odcl(img_num, odcl_data, img_crop):
    print("Tryna submit image: ", img_num)
    img = cv2.imread("assets/img/" + str(img_num) + ".jpg")
    x,y,w,h = img_crop['x'], img_crop['y'], img_crop['w'], img_crop['h']
    print(x,y,w,h)
    crop = img[y:y+h, x:x+h]
    cv2.imwrite("assets/crop/" + str(img_num) + ".jpg", crop)

def encode_img(img):
    pass

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    DIR = 'assets/img'
    files = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR,name))]
    return json.dumps({'highest': len(files)})

@app.route('/receiver', methods = ["GET", "POST"])
def receiver():
    print('hi')
    if request.method == "POST":
        data = request.get_json()
        img_num = data['img_num']
        odcl_data = data['odcl']
        img_crop = data['img_crop']
        print("DICTIONARY DATA")
        print(data)
        submit_odcl(img_num, odcl_data, img_crop)
#        submit_odcl(img_url, odcl_data)
    return 'OK'


if __name__ == "__main__":
    main()
