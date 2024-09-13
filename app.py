import io

from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from googletrans import Translator
import keras
from tensorflow.keras import models
from sklearn.preprocessing import LabelEncoder
import numpy as np
from PIL import Image
import pickle
from sklearn.feature_extraction.text import HashingVectorizer
import cv2

import json

translator = Translator()
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
    if 'fileInput' not in request.files:
        return jsonify({"error": "No file provided!"}), 400

    file = request.files['fileInput']
    description = request.form.get('inputData', '')

    if file.filename == '':
        return jsonify({"error": "No file selected!"}), 400

    image = file.read()
    description = translator.translate(description, dest="en").text
    image = cv2.resize(np.array(Image.open(io.BytesIO(image))), (128, 128))
    TEXT_DATA = [vectorizer.transform([description]).toarray()]

    predict = model.predict(x=[np.array([image]), TEXT_DATA])
    metka = predict.argmax(axis=-1)[0]
    label_encoder_dd = label_encoder.inverse_transform([metka])[0]

    predict = np.sort(predict)
    response = {'answer': str(label_encoder_dd)}
    return response


if __name__ == '__main__':
    app.run(debug=True)
