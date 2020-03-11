import os
import cv2
import json
from handler import Handler
from flask_cors import CORS
from flask import Flask, jsonify, render_template, request

config = json.load(open("config.json"))
#handler = Handler(config)
#handler.init_socket()


def watch_files():
    extra_dirs = ['.']
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in os.walk(extra_dir):
            for filename in files:
                filename = os.path.join(dirname, filename)
                if os.path.isfile(filename):
                    extra_files.append(filename)
    return extra_files


app = Flask("__name__", static_folder="static")
CORS(app)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    DIR = 'static/img'
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


def main():
    app.secret_key = 'password'
    app.run(debug=True, port=5000, extra_files=watch_files())

if __name__ == '__main__':
    main()

#while True:
#    inp = input().split()
#    if inp[0] == "SUBMIT":
#        num = int(inp[1])
#        data = {"LKJFSDLKJDFSKJL": "JBJHUSHDUDSJLK"}
#        handler.submit_odcl("assets/images/submission" + str(num) + ".jpg", data)