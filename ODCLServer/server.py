from PIL import Image
from flask import Flask, render_template, jsonify
from flask_cors import CORS
import json
import threading
import os
#from interop_helpers import *

# test commit

# img = Image.open("submit.jpg")
# img = img.crop((0, 0, img.size[0] / 2, img.size[1] / 2))
# submission_id = "submission1.jpg"
# img.convert('RGB').save(submission_id)

global data, curr_id, images
curr_id = 0
images = []
for filename in os.listdir(os.path.abspath('ODCLServer/static')):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        images.append("/static/" + filename)
    else:
        continue
# print(images)
# print(len(images))
data = []
odcl_data = {
    "id": curr_id,
    "img_path": images[curr_id],
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


def update_thread():
    import time
    while True:
        # time.sleep(4)
        print("Updated")
        global data, curr_id, images
        images = []
        for filename in os.listdir(os.path.abspath('ODCLServer/static')):
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


if __name__ == '__main__':
    update = threading.Thread(target=update_thread)
    update.daemon = True
    update.start()
    app.secret_key = 'password'
    app.run(debug=True)


# with open('submission1.txt', 'w') as outfile:
#     json.dump(data, outfile)
# test commit
