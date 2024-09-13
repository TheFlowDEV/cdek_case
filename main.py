from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os

import keras
from tensorflow.keras import models
from sklearn.preprocessing import LabelEncoder
import numpy as np
from PIL import Image
import pickle
from sklearn.feature_extraction.text import HashingVectorizer
import cv2

import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
model = models.load_model('AI_CDEK.keras')

with open("vec_and_le.pkl", 'rb') as f:
    label_encoder, vectorizer = pickle.load(f)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided!"}), 400

    file = request.files['file']
    description = request.form.get('description', '')

    # if file.filename == '':
    #     return jsonify({"error": "No file selected!"}), 400

    # filename = secure_filename(file.filename)
    # print(filename)
    # file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # file.save(file_path)
    # image = Image.open(file_path)
    # image.resize(128,128)
    # TEXT_DATA = [vectorizer.transform([description]).toarray()]
    # predict = model.predict(x=[np.array([image]),TEXT_DATA])
    # metka = predict.argmax(axis=-1)[0]
    # label_encoder_dd = label_encoder.inverse_transform([metka])

    # predict = np.sort(predict)
    # print(label_encoder_dd)

    # return render_template('index.html', result=label_encoder_dd)


if __name__ == '__main__':
    app.run(debug=True)

