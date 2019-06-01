import json
import time
import threading
import socket
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import cv2
import numpy as np

MY_IP = '127.0.0.1'  # Need to change to IP of comms computer
PORT = 5005
BUFFER_SIZE = 1024  # Can make this lower if we need speed



global image_num
image_num = 0

def save_image(image_string):
    global image_num
#    image_string = image_bytes.decode('utf-8')
    nparr = np.fromstring(image_string, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite("assets/LiveImage" + str(image_num) + ".png", img)
    image_num += 1

def connect_comms():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((TCP_IP, PORT))
	sock.listen(1)
	global conn
	conn, addr = sock.accept()


#def sock_recv():
#	global
#    while True:
#        temp = conn.recv(1000000)
#		ingest(temp.decode('utf-8'))
#        save_image(temp)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    print('hi')
    return 'hi'

if __name__ == "__main__":
	connect_comms()
#	sock_thread = threading.Thread(target=sock_recv)
#	sock_thread.start()
	app = Flask("__name__", static_folder="assets")
	# Prevent CORS errors
	CORS(app)
    app.run()
