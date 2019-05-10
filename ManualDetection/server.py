import json
import time
import threading
import socket
from flask import Flask, jsonify, render_template, request
from flask_caching import Cache
from flask_cors import CORS
import cv2
import numpy as np
import base64

global x
x = 1
COMMS_IP = '127.0.0.1'  # Need to change to IP of comms computer
PORT = 5005
MY_IP = '127.0.0.1'
BUFFER_SIZE = 10000000  # Can make this lower if we need speed

global sock, image_num
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
image_num = 0
app = Flask("__name__", static_folder="assets")

def main():
    connect_comms()

    cache = Cache(config={'CACHE_TYPE': 'redis'})
    app.config["CACHE_TYPE"] = "null"
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    # Prevent CORS errors
    CORS(app)
    app.run()
    x = 0

def save_image(img_string):
    global image_num
#    img_bytes = base64.b64encode(img_string)
    nparr = np.array(img_string, dtype=np.uint8)
    print("Numpy shape:",nparr.shape)
#    nparr = np.fromstring(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    print("Image shape",img.shape)
    cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite("assets/img/image_" + str(image_num) + ".png", img)
    image_num += 1
    print(image_num)

def connect_comms():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Over Internet, TCP protocol
    sock.connect((COMMS_IP, PORT)) 

    listen_thread = threading.Thread(target=listen)
    listen_thread.start()

def listen():
    global sock
    while True:
        data_bytes = sock.recv(BUFFER_SIZE)
        print("RECEIVED")
        data_string = data_bytes.decode('utf-8')
        data_dict = json.loads(data_string)
        ingest_thread = threading.Thread(target=command_ingest, args=(data_dict,))
        ingest_thread.start()

def command_ingest(message_dict):
    header = message_dict['HEADER']
    if header == "CAMERA_IMAGE":
        save_image(message_dict['MESSAGE'])
    elif header == "BUFFER":
        BUFFER_SIZE = int(message_dict['MESSAGE'])
    elif header == "PRINT":
        print(message_dict['MESSAGE'])
    else:
        print("Unkown header:", header)

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

# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == "__main__":
#    cache.init_app(app)
#    cache.clear()
    main()
#    with app.app_context():
#        cache.clear()
