from PIL import Image
from flask import Flask, render_template, jsonify
from flask_cors import CORS
import json
import threading
import os
#from interop_helpers import *

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

@app.route('/submissions')
def submissions():
    return render_template('submissions.html')

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


def pseudo_update():
    import time
    while True:
        # time.sleep(4)
        print("Updated")
        global data, curr_id, images
        images = []
        for filename in os.listdir(os.path.abspath('static')):
            if filename.endswith(".png") or filename.endswith(".jpg"):
                images.append("/static/" + filename)
            else:
                continue

        # print("1: ", curr_id)
        if(curr_id <= len(images) - 1):
            curr_id = curr_id + 1
        else:
            break
        # print("2: ", curr_id)
        data.append({i:odcl_data[i] for i in odcl_data})
        data[-1]["id"] = curr_id
        data[-1]["img_path"] = images[curr_id-1]
        # print(data["id"])
        # print(data["img_path"])

def sock_thread():
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((MY_IP, PORT))
    sock.listen(1)
    conn, addr = sock.accept()
    while True:
        img_data = conn.recv()
        img_data = 



def real_update():
    while True:
        global data, displayed_images, curr_id
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


if __name__ == '__main__':
    update = threading.Thread(target=real_update)
#    update = threading.Thread(target=pseudo_update)
    update.daemon = True
    update.start()
    app.secret_key = 'password'
    app.run(debug=True)
