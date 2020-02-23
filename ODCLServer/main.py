from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import cv2
import os
import socket, base64, pickle, json
import threading, logging
import time
import numpy as np
from collections import deque

from auvsi_suas.client import client
from auvsi_suas.proto import interop_api_pb2
#from interop_helpers import *

# Don't print the Flask debugging information in terminal
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

MY_IP, PORT = '127.0.0.1', 5010

global data, displayed_images, curr_id
displayed_images = set()
curr_id = 0
# print(images)
# print(len(images))
data = []
odcl_data = {
    "mission": 1,
    "type": "STANDARD",
    "latitude": 38,
    "longitude": -76,
    "orientation": "N",
    "shape": "RECTANGLE",
    "shapeColor": "RED",
    "alphanumeric": "T",
    "alphanumericColor": "GREEN",
    "autonomous": True,
    "submitted": False,
    "discarded": False
}

app = Flask(__name__)
CORS(app)
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/sub.js')
def sub():
    return render_template('sub.js')

@app.route('/main.js')
def main():
    return render_template('main.js')

@app.route('/post')
def interactive():
    global data
    submit_to_interop()
    return jsonify(data)

def encode_img(img):
    _, encoded = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 80])
    encoded = pickle.dumps(encoded)
    encoded_b64 = base64.encodebytes(encoded)
    encoded_str = encoded_b64.decode('ascii')
    return encoded_str

def decode_img(data):
    encoded_b64 = data.encode('ascii')
    encoded = base64.decodebytes(encoded_b64)
    img = pickle.loads(encoded)
    img = cv2.imdecode(img, 1)
    return img

def connect_interop_server():
    global clent
    config = json.load(open("../config.json"))
    client = client.Client(url=config["interop_url"],
                       username='tjuav',
                       password='getmeout')

def connect_server():
    global conn, sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((MY_IP, PORT))
    sock.listen(1)
    conn, addr = sock.accept()

def sock_comms():
    global conn, sock
    print("Running socket stuff")
    img_num = 1
    while True:
        packet_str = conn.recv(100000)
        print("Packet: ", packet_str)
        packet = json.loads(packet_str.decode())
        odcl_data = packet["odcl_data"]
        img = decode_img(packet["image"])
        cv2.imwrite("static/submission" + str(img_num) + ".jpg", img)
        print("WROTE THE IMAGE TO static/submission" + str(img_num) + ".jpg")
        img_num += 1

def send_socket(filename):
    global conn, sock
    # packet = {}
    print(filename)
    img = cv2.imread("jetson_imgs/" + filename)
    print(img)
    encoded = encode_img(img)
    encoded_b64 = base64.encodebytes(encoded)
    # packet["image"] = encoded_b64.decode('ascii')
    # packet["odcl_data"] = odcl_data
    # packet_str = json.dumps(packet)
    conn.send(encoded_b64)
    # print(packet)

def real_update():
    time.sleep(2)
    imgs = []
    while True:
        global data, displayed_images, curr_id
        check_imgs = os.listdir(os.path.abspath('jetson_imgs'))
        new_index = len(imgs)
        if imgs != check_imgs:
            for filename in check_imgs[new_index:]:
                if filename.endswith(".png") or filename.endswith(".jpg"):
                    print("Sending " + filename + "...")
                    time.sleep(0.25)
                    send_socket(filename)
                    print(filename + " sent!")
                    time.sleep(0.25)
            imgs = check_imgs
        images = []
        for filename in os.listdir(os.path.abspath('static')):
            if filename.endswith(".png") or filename.endswith(".jpg"):
                if filename in displayed_images:
                    continue

                print("Updated")
                odcl_dict = {i:odcl_data[i] for i in odcl_data}
                odcl_dict["id"] = curr_id
                odcl_dict["img_path"] = "/static/" + filename
                data.append(odcl_dict)
                curr_id += 1
                displayed_images.add(filename)

def submit_to_interop(curr_id):
    global data
    odcl_dict = data[curr_id]
    odlc = interop_api_pb2.Odlc()
    odlc.type = interop_api_pb2.Odlc.STANDARD
    odlc.latitude = odcl_dict["latitude"]
    odlc.longitude = odcl_dict["longitude"]
    odlc.orientation = odcl_dict["orientation"]
    odlc.shape = odcl_dict["shape"]
    odlc.shape_color = odcl_dict["shape_color"]
    odlc.alphanumeric = odcl_dict["alphanumeric"]
    odlc.alphanumeric_color = odcl_dict["alphanumeric_color"]

    odlc = client.post_odlc(odlc)

    with open(odcl_dict["img_path"], 'rb') as f:
        image_data = f.read()
        client.put_odlc_image(odlc.id, image_data)


<<<<<<< HEAD
def main():
    update = threading.Thread(target=real_update)
    update.daemon = True
    update.start()
=======
if __name__ == '__main__':
    connect_server()
    connect_interop_server()
>>>>>>> b25a3feca95bc0dcb28f93400a65a36cce85a472
    sock_thread = threading.Thread(target=sock_comms)
    sock_thread.daemon = True
    sock_thread.start()
    update = threading.Thread(target=real_update)
    # update = threading.Thread(target=pseudo_update)
    update.daemon = True
    update.start()
    app.secret_key = 'password'
<<<<<<< HEAD
    app.run(debug=False, port=5000)

if __name__ == '__main__':
    main()
=======
    app.run(debug=False, port=5000)
>>>>>>> b25a3feca95bc0dcb28f93400a65a36cce85a472
