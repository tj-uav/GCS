from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import random
import math
import socket
import json
import time

#TCP_IP = '127.0.0.1'  # Need to change to IP of groundstation
#TCP_PORT = 5005
#BUFFER_SIZE = 1024  # Can make this lower if we need speed

#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.bind((TCP_IP, TCP_PORT))
#sock.listen(1)

#conn, addr = sock.accept()

app = Flask("__name__", static_folder="assets")
# Prevent CORS errors
CORS(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/data")
def data():
    print('hi')
    return 'hi'


if __name__ == "__main__":
    app.run()
