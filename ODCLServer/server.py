from PIL import Image
from flask import Flask, render_template, jsonify
from flask_cors import CORS
import json
import threading
#from interop_helpers import *

# img = Image.open("submit.jpg")
# img = img.crop((0, 0, img.size[0] / 2, img.size[1] / 2))
# submission_id = "submission1.jpg"
# img.convert('RGB').save(submission_id)

global data
data = {
    "id": 0,
    "img_path": "/static/submit.jpg",
    "mission": 1,
    "type": "STANDARD",
    "latitude": 38,
    "longitude": -76,
    "orientation": "N",
    "shape": "RECTANGLE",
    "shapeColor": "RED",
    "alphanumeric": "T",
    "alphanumericColor": "GREEN",
    "autonomous": True
}

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


def update_thread():
    import time
    time.sleep(4)
    print("Updated")
    global data
    data = {
        "id": 1,
        "img_path": "/static/submit2.png",
        "mission": 1,
        "type": "STANDARD",
        "latitude": 42,
        "longitude": -71,
        "orientation": "W",
        "shape": "SQUARE",
        "shapeColor": "GREEN",
        "alpha": "B",
        "alphaColor": "YELLOW",
        "autonomous": True
    }


if __name__ == '__main__':
    update = threading.Thread(target=update_thread)
    update.daemon = True
    update.start()
    app.secret_key = 'password'
    app.run(debug=True)


# with open('submission1.txt', 'w') as outfile:
#     json.dump(data, outfile)
# test commit
