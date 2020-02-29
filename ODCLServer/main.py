from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import cv2
import os
import socket, base64, pickle, json
import threading, logging
import time
import numpy as np
from collections import deque


# Don't print the Flask debugging information in terminal
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Load constants from config file
config = json.load(open("config.json"))
USE_INTEROP, INTEROP_URL = config['use_interop'], config['interop_url']


global data, curr_id
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
    return jsonify(data)


def display_update():
    displayed_images = {}
    while True:
        for filename in os.listdir(os.path.abspath('static')):
            if filename in displayed_images:
                continue
            if filename.endswith(".png") or filename.endswith(".jpg"):
                odcl_dict = {i:odcl_data[i] for i in odcl_data}
                odcl_dict["id"] = curr_id
                odcl_dict["img_path"] = "/static/" + filename
                data.append(odcl_dict)
                curr_id += 1
                displayed_images.add(filename)
                print("Updated")



def main():
    update = threading.Thread(target=real_update)
    update.daemon = True
    update.start()
    sock_thread = threading.Thread(target=sock_comms)
    sock_thread.daemon = True
    sock_thread.start()
    update = threading.Thread(target=real_update)
    # update = threading.Thread(target=pseudo_update)
    update.daemon = True
    update.start()
    app.secret_key = 'password'
    app.run(debug=False, port=5000)

if __name__ == '__main__':
    main()
