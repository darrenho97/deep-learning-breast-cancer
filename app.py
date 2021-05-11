import numpy as np
from flask import Flask, request, jsonify, render_template
from flask import Flask, render_template, request, redirect, flash, url_for
import pickle
import urllib.request
from werkzeug.utils import secure_filename
from predict import getPrediction
import os

app = Flask(__name__)
app.secret_key = "super secret key"


UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static\\uploads')

print(UPLOAD_FOLDER)

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html', pre_click=True)

@app.route('/', methods=['POST'])
def submit_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            getPrediction(filename)
            label = getPrediction(filename)
            print(label)
            flash(label)
            flash(filename)
            label = "Your Diagnosis: " + label[0]
            data = [label]
            return render_template('index.html', data=data, pre_click=False, filename=filename)


@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)

	return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == '__main__':
    app.debug = True
    app.run()