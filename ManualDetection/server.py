import json
import time
import threading
import socket
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import cv2
import numpy as np
import os
from collections import deque

IPS = {"COMMS_COMP":'127.0.0.1'}#, "MISSION_PLANNER":'127.0.0.1', "JETSON": '127.0.0.1', "MANUAL_DETECTION": '127.0.0.1', "MANUAL_CLASSIFICATION": '127.0.0.1'} #Change to actual values
PORT = 5005
MY_IP = '127.0.0.1'
BUFFER_SIZE = 10000000  # Can make this lower if we need speed
IMAGE_BASENAME = "assets/img/"
IMAGE_ENDING = ".png"

IMAGES_SAVED = []

global sock, image_recent_num
MESSAGE_QUEUE = deque([])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
image_recent_num = 0
app = Flask("__name__", static_folder="assets")

def main():
    connect_comms()
#    sending_thread = threading.Thread(target=send_data)
#    sending_thread.start()

    app.config["CACHE_TYPE"] = "null"
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    # Prevent CORS errors
    CORS(app)
    app.run()
    enqueue(destination=IPS['COMMS_COMP'], header='TERMINATE', message='')
    time.sleep(0.5)
    os._exit(1)
def listenImg():
    sock.listen(1)
    yeet, skeet = sock.accept()
    print("Listening to " + str(skeet))
    while True:
        raw = yeet.recv(BUFFER_SIZE)
        arr = np.fromstring(raw, np.uint8)
        save_image(cv2.imdecode(arr, cv2.CV_LOAD_IMAGE_COLOR))
        print("image saved !!!1!!1!!")
def delete_image(img_num):
    filename = IMAGE_BASENAME + str(img_num) + IMAGE_ENDING
    try:
        os.remove(filename)
        IMAGES_SAVED.remove(img_num)
    except:
        pass

def save_image(img_string):
    global image_recent_num
    nparr = np.array(img_string, dtype=np.uint8)
    print("Numpy shape:",nparr.shape)
#    nparr = np.fromstring(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    print("Image shape",img.shape)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(IMAGE_BASENAME + str(image_recent_num) + IMAGE_ENDING, img)
    IMAGES_SAVED.append(image_recent_num)
    image_recent_num += 1
    print(image_recent_num)

def connect_comms():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Over Internet, TCP protocol
    sock.bind((IPS['COMMS_COMP'], PORT))
    listen_thread = threading.Thread(target=listenImg)
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

def send_data():
    #Check if MESSAGE_QUEUE is empty. If it is not empty, send that message to the corresponding device
    while True:
        if MESSAGE_QUEUE:
            nextMessage = MESSAGE_QUEUE.popleft()
            print(nextMessage)
            DESTINATION_IP = nextMessage['DESTINATION']
            nextMessage_json = json.dumps(nextMessage)
            nextMessage_bytes = nextMessage_json.encode('utf-8')
            sock.send(nextMessage_bytes)
            time.sleep(0.5) #Can be changed

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

def enqueue(destination, header, message, subheader = None):
    to_send = {}
    to_send['SOURCE'] = MY_IP
    to_send['DESTINATION'] = destination
    to_send['HEADER'] = header
    to_send['MESSAGE'] = message
    if subheader:
        to_send['SUBHEADER'] = subheader
    MESSAGE_QUEUE.append(to_send)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/receiver', methods = ["GET", "POST"])
def receiver():
    if request.method == "POST":
        data = request.get_json()
        lowest = data['lowest']
        print(lowest)
        i = lowest - 1
        while i in IMAGES_SAVED:
            delete_image(i)
            i -= 1

    return 'OK'

@app.route("/data")
def data():
    global image_recent_num
    return jsonify({"highest":image_recent_num})

# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == "__main__":
    main()
