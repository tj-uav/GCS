from flask import Flask, render_template, jsonify
from flask_cors import CORS
import cv2
import os
import socket, base64, pickle, json
import threading, logging
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

def sock_comms():
    print("Running socket stuff")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((MY_IP, PORT))
    sock.listen(1)
    conn, addr = sock.accept()
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


def main():
    update = threading.Thread(target=real_update)
    update.daemon = True
    update.start()
    sock_thread = threading.Thread(target=sock_comms)
#    update = threading.Thread(target=pseudo_update)
    sock_thread.daemon = True
    sock_thread.start()
    app.secret_key = 'password'
    app.run(debug=False, port=5000)

if __name__ == '__main__':
    main()