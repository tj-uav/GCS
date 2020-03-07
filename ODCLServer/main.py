import os
import logging
from handler import Handler
from flask_cors import CORS
import json
from flask import Flask, render_template, jsonify, request

print(os.getcwd())

# Don't print the Flask debugging information in terminal
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Load constants from config file
config = json.load(open("config.json"))

#handler = Handler(config)
#handler.init_socket()
#if config['use_interop']:
#    handler.init_interop()

global data
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
data.append(odcl_data)

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

app = Flask(__name__)
CORS(app)
@app.route('/')
def index():
    print("HI")
    return render_template("index.html")

@app.route('/post')
def interactive():
    return jsonify(data)

def main():
    app.secret_key = 'password'
    app.run(debug=True, port=5000, extra_files=watch_files())

if __name__ == '__main__':
    main()
