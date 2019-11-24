from PIL import Image
from flask import Flask, render_template, jsonify
from flask_cors import CORS
import json

# img = Image.open("submit.jpg")
# img = img.crop((0, 0, img.size[0] / 2, img.size[1] / 2))
# submission_id = "submission1.jpg"
# img.convert('RGB').save(submission_id)

characteristics = {
    "id": 0,
    "mission": 1,
    "type": "STANDARD",
    "latitude": 38,
    "longitude": -76,
    "orientation": "N",
    "shape": "RECTANGLE",
    "shapeColor": "RED",
    "alpha": "A",
    "alphaColor": "BLUE",
    "autonomous": True
}

app = Flask(__name__)
CORS(app)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recent')
def recent():
	return jsonify(characteristics)

@app.route('/thing.js')
def thing():
    return render_template('thing.js')

if __name__ == '__main__':
    app.secret_key='password'
    app.run(debug=True)
    while True:
        if input() == "add":
            characteristics = {
                "id": 2,
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

            


# with open('submission1.txt', 'w') as outfile:
#     json.dump(characteristics, outfile)
