import os
from flask import Flask, jsonify, render_template, redirect, url_for, send_file, send_from_directory, request

app = Flask(__name__)

"""
Sets default action to perform with no specified route
    images: array containing paths to all image files in images directory
    os.path.abspath: returns absolute path of directory to retrieve image files from
    render_template: renders specified template (html) on web page
        images input: takes list of filepaths to display imgs
"""
@app.route("/")
def home():
    images = []
    for filename in os.listdir(os.path.abspath('ODCLServer/FlaskServer/static/images')):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            images.append(os.path.join('/static/images/', filename))
        else:
            continue
    return render_template("home.html", images=images)

if __name__ == "__main__":
    app.run(debug=True)