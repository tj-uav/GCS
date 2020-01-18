from PIL import Image
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import threading
import socket
import os
from collections import deque
import cv2
from connection import Connection

ODCL_COMPUTERS = 1

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/classification')
def classification():
    return classification_queue[0]

@app.route('/next', methods = ["GET", "POST"])
def next():
    print('hi')
    if request.method == "POST":
        data = request.get_json()
        img_num = data['img_num']
        odcl_data = data['odcl']
        img_crop = data['img_crop']
        print("DICTIONARY DATA")
        print(data)



def create_connections():
    addresses = config["Addresses"]
    num_computers = len(addresses) - 1
    inv_addresses = {}
    for name in addresses:
        ip = addresses[name]
        inv_addresses[ip] = name

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(addresses["Communication"])
    sock.listen(num_computers)
    connections = {}
    for i in range(num_computers):
        conn, addr = sock.accept()
        print("Incoming connection from", addr)
        assert(addr in inv_addresses)
        name = inv_addresses[addr]
        connections[name] = Connection(name, conn)
    return connections

def decode_image(img):
    pass
   
def send(name, header, message):
    global connections
    conn = connections[name]
    conn.send(header, message)

def ingest(conn, name, packet):
    # The comms computer won't be receiving anything from MP computer, because MP computer can directly communicate with interop
    header = packet['Header']
    message = packet['Message']
    if name == 'Jetson':
        if header == 'Image':
            img = decode_image(message)
            addresses = config["Addresses"]
            global odcl_comp
            odcl_comp %= ODCL_COMPUTERS
            odcl_comp += 1
            addr = addresses['ODCL_' + str(odcl_comp)]

        elif header == 'Buffer':
            conn.buffer = message

    elif 'ODCL' in name:
        if header == 'Submission':
            img = decode_image(message)
            global classification_queue
            num_classifications = os.listdir('static/classification')
            filepath = 'static/classification/image' + str(num_classifications) + '.jpg'
            cv2.imwrite(filepath, img)
            classification_queue.append(filepath)


def ingest_thread(connections):
    while True:
        for conn in connections:
            while len(conn.ingest_queue):
                name = conn.name
                packet = conn.popleft()
                ingest(connections, conn, name, packet)


if __name__ == '__main__':
    global config, submission_list, classification_queue, data, odcl_comp, connections
    config = json.load(open('config.json'))
    submission_list = []
    classification_queue = deque([])
    data = {}
    odcl_comp = 0
#    connections = create_connections()

    app.secret_key = 'password'
    app.run(debug=True)
