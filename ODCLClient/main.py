import os
import cv2
import json
import time
import logging
import numpy as np
from handler import Handler
from flask_cors import CORS
from flask import Flask, jsonify, render_template, request

config = json.load(open("config.json"))
handler = Handler(config)
handler.init_socket()

app = Flask("__name__", static_folder="assets")
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    DIR = 'assets/img'
    files = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR,name))]
    print(len(files), files)
    return json.dumps({'highest': len(files)})

@app.route('/receiver', methods = ["GET", "POST"])
def receiver():
    print('hi')
    if request.method == "POST":
        data = request.get_json()
        img_num = data['img_num']
        odcl_data = data['odcl']
        img_crop = data['img_crop']
        print("DICTIONARY DATA")
        print(data)
#        submit_odcl(img_url, odcl_data)
    return 'OK'

#app.run(port = 5005)
while True:
    inp = input().split()
    if inp[0] == "SUBMIT":
        num = int(inp[1])
        data = {"LKJFSDLKJDFSKJL": "JBJHUSHDUDSJLK"}
        handler.submit_odcl("assets/images/submission" + str(num) + ".jpg", data)