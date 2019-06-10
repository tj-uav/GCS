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

from auvsi_suas.client import client
from auvsi_suas.proto import interop_api_pb2
from google.protobuf import json_format

IMAGE_BASENAME = 'assets/img/'
IMAGE_ENDING = '.png'
IMAGES_SAVED = {}

CLASSIFICATION_IP = '127.0.0.1'  # Need to change to IP of comms computer
PORT = 5050
BUFFER_SIZE = 1024000  # Can make this lower if we need speed

ODCL_SHAPECONV = {'CIRCLE' : 1, 'SEMICRICLE' : 2, 'QUARTER_CIRCLE' : 3, 'TRIANGLE' : 4, 'SQUARE' : 5, 'RECTANGLE' : 6, 'TRAPEZOID' : 7, 'PENTAGON' : 8, 'HEXAGON' : 9, 'HEPTAGON' : 10, 'OCTAGON' : 11, 'STAR' : 12, 'CROSS' : 13}
ODCL_COLORCONV = {'WHITE' : 1, 'BLACK' : 2, 'GRAY' : 3, 'RED' : 4, 'BLUE' : 5, 'GREEN' : 6, 'YELLOW' : 7, 'PURPLE' : 8, 'BROWN' : 9, 'ORANGE' : 10}
ODCL_ORIENTATIONCONV = {'N' : 1, 'NE' : 2, 'E' : 3, 'SE' : 4, 'S' : 5, 'SW' : 6, 'W' : 7, 'NW' : 8}

writepath = "data.txt"
writer = open(writepath, "w+")

global app, image_num, MISSION_ID
app = Flask("__name__", static_folder="assets")
image_num = 1
MISSION_ID = 1

def main():
    global app
    connect_interop(interop_url='http://98.169.139.31:8000', username='testuser', password='testpass')
    print('Connected to interop')
	# Prevent CORS errors
    CORS(app)
    app.run()

"""
def save_image(image_string, img_geoloc):
    global image_num
#    image_string = image_bytes.decode('utf-8')
    nparr = np.fromstring(image_string, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#    cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(IMAGE_BASENAME + str(image_num) + IMAGE_ENDING, img)
    if img_geoloc:
        IMAGES_SAVED[image_recent_num] = img_geoloc
    image_num += 1

def delete_image(img_num):
    filename = IMAGE_BASENAME + str(img_num) + IMAGE_ENDING
    try:
        os.remove(filename)
        if i in IMAGES_SAVED:
            IMAGES_SAVED.remove(i)
    except:
        pass
"""

def make_odlc_from_data(message_data):    
    odlc = interop_api_pb2.Odlc()
    odlc.mission = MISSION_ID
#    if 'type' in message_data and isinstance(message_data['type'], str):
#        odlc.type = message_data['type']
    print(message_data)
    for key in message_data:
        print(key, message_data[key], type(message_data[key]))
    odlc.type = interop_api_pb2.Odlc.STANDARD
    if 'latitude' in message_data:
        odlc.latitude = message_data['latitude']
    if 'longitude' in message_data:
        odlc.longitude = message_data['longitude']
    if 'orientation' in message_data and message_data['orientation'] in ODCL_ORIENTATIONCONV:
        odlc.orientation = ODCL_ORIENTATIONCONV[message_data['orientation']]
    if 'shape' in message_data and message_data['shape'] in ODCL_SHAPECONV:
        odlc.shape = ODCL_SHAPECONV[message_data['shape']]
    if 'shape_color' in message_data and message_data['shape_color'] in ODCL_COLORCONV:
        odlc.shape_color = ODCL_COLORCONV[message_data['shape_color']]
    if 'alphanumeric' in message_data and isinstance(message_data['alphanumeric'], str):
        odlc.alphanumeric = message_data['alphanumeric']
    if 'alphanumeric_color' in message_data and message_data['alphanumeric_color'] in ODCL_COLORCONV:
        odlc.alphanumeric_color = ODCL_COLORCONV[message_data['alphanumeric_color']]
    return odlc

def submit_odcl(img_num, data):
#    if img_num not in IMAGES_SAVED:
#        print("Image not found in directory")
#        return
    odlc_object = make_odlc_from_data(data)
    odlc_object = cl.post_odlc(odlc_object).result()
    filename = IMAGE_BASENAME + str(img_num) + IMAGE_ENDING
    with open(filename, 'rb') as f:
        image_data = f.read()
        cl.post_odlc_image(odlc_object.id, image_data)

def connect_comms():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Over Internet, TCP protocol
    sock.connect((CLASSIFICATION_IP, PORT))

def connect_interop(interop_url, username, password):
    global cl
    cl = client.AsyncClient(url=interop_url,
                       username=username,
                       password=password)

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
        submit_odcl(img_num, odcl_data)
    return 'OK'


if __name__ == "__main__":
    main()