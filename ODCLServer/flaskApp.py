from PIL import Image
from flask import Flask, render_template, jsonify
import json

# img = Image.open("submit.jpg")
# img = img.crop((0, 0, img.size[0] / 2, img.size[1] / 2))
# submission_id = "submission1.jpg"
# img.convert('RGB').save(submission_id)

data = {
    "id": 1,
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
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/thing.js')
def thing():
    return render_template('thing.js', data=data)

@app.route('/post')
def interactive():
	return jsonify(data)

if __name__ == '__main__':
    app.secret_key='password'
    app.run(debug=True)

# with open('submission1.txt', 'w') as outfile:
#     json.dump(data, outfile)
