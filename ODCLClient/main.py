import json
import time
import threading
import socket
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import cv2
import numpy as np
from collections import deque
import pickle
import base64
import logging
import os

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

IMAGE_BASENAME = 'assets/img/'
IMAGE_ENDING = '.jpg'

BUFFER_SIZE = 1024000  # Can make this lower if we need speed

ODCL_SHAPECONV = {'CIRCLE' : 1, 'SEMICRICLE' : 2, 'QUARTER_CIRCLE' : 3, 'TRIANGLE' : 4, 'SQUARE' : 5, 'RECTANGLE' : 6, 'TRAPEZOID' : 7, 'PENTAGON' : 8, 'HEXAGON' : 9, 'HEPTAGON' : 10, 'OCTAGON' : 11, 'STAR' : 12, 'CROSS' : 13}
ODCL_COLORCONV = {'WHITE' : 1, 'BLACK' : 2, 'GRAY' : 3, 'RED' : 4, 'BLUE' : 5, 'GREEN' : 6, 'YELLOW' : 7, 'PURPLE' : 8, 'BROWN' : 9, 'ORANGE' : 10}
ODCL_ORIENTATIONCONV = {'N' : 1, 'NE' : 2, 'E' : 3, 'SE' : 4, 'S' : 5, 'SW' : 6, 'W' : 7, 'NW' : 8}

SERVER_IP, PORT = '127.0.0.1', 5010
IMG_IP, IMG_PORT = '127.0.0.1', 5015
MISSION_ID = 3

global app
app = Flask("__name__", static_folder="assets")

def main():
    global app
    connect_server()
    print('Connected to comms comp')
    sock_thread = threading.Thread(target=sock_comms)
    sock_thread.daemon = True
    sock_thread.start()
	# Prevent CORS errors
    CORS(app)
    app.run(debug=False, port=5005)

def sock_comms():
    print("Running socket stuff")
    sock_img = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_img.bind((IMG_IP, IMG_PORT))
    sock_img.listen(1)
    conn, addr = sock_img.accept()
    img_num = 1
    while True:
        packet_str = conn.recv(100000)
        print("Packet: ", packet_str)
        packet = json.loads(packet_str.decode())
        odcl_data = packet["odcl_data"]
        encoded_b64 = packet["image"].encode('ascii')
        encoded = base64.decodebytes(encoded_b64)
        img = decode_img(encoded)
        cv2.imwrite("assets/img/" + str(img_num) + ".jpg", img)
        print("WROTE THE IMAGE TO assets/img" + str(img_num) + ".jpg")
        img_num += 1

def connect_server():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, PORT))
#    recv_thread = threading.Thread(target=img_recv_loop)
#    recv_thread.daemon = True
#    recv_thread.start()

def send_socket(img, data):
    global sock
    packet = {}
    encoded = encode_img(img)
    encoded_b64 = base64.encodebytes(encoded)
    packet["image"] = encoded_b64.decode('ascii')
    packet["odcl_data"] = data
    packet_str = json.dumps(packet)
    sock.send(packet_str.encode())
#    print(packet)

def img_recv_loop():
    image_num = 8
    global sock
    while True:
        buffer = int(sock.recv(1024).decode())
        data = sock.recv(BUFFER)
        img = decode_img(data)
        cv2.imwrite("img/" + image_num + ".jpg")
        image_num += 1

def encode_img(img):
    _, encoded = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 80])
    return pickle.dumps(encoded)

def decode_img(data):
    img = pickle.loads(data)
    img = cv2.imdecode(img, 1)
    return img

def submit_odcl(img_num, odcl_data, img_crop):
    print("Tryna submit image: ", img_num)
    img = cv2.imread("assets/img/" + str(img_num) + ".jpg")
    x,y,w,h = img_crop['x'], img_crop['y'], img_crop['w'], img_crop['h']
    scaleY, scaleX, _ = img.shape
    x = int(x * scaleX)
    y = int(y * scaleY)
    w = int(w * scaleX)
    h = int(h * scaleY)
    
    crop = img[y:y+h, x:x+w]
    send_socket(crop, odcl_data)

#    cv2.imwrite("assets/crop/" + str(img_num) + ".jpg", crop)

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
