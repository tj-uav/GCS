import os
import cv2
import time
import numpy as np
import threading, logging
from handler import Handler
from flask_cors import CORS
from collections import deque
import socket, base64, pickle, json
from flask import Flask, render_template, jsonify, request


# Don't print the Flask debugging information in terminal
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Load constants from config file
config = json.load(open("config.json"))

handler = Handler(config)
handler.init_socket()


print(1/0)

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
