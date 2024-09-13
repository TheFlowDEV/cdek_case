import io

from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
import re
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

def clean_text(s):
    return re.sub(r'<.*?>', '', s)


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
    description = translator.translate(clean_text(description), dest="en").text
    image = cv2.resize(np.array(Image.open(io.BytesIO(image))), (128, 128))
    TEXT_DATA = [vectorizer.transform([description]).toarray()]

    predict = model.predict(x=[np.array([image]), TEXT_DATA])
    metka = predict.argmax(axis=-1)[0]
    label_encoder_dd = label_encoder.inverse_transform([metka])[0]

    # predict = np.sort(predict)

    top_10_indices = np.argsort(predict[0])[::-1][:1]

    top_10_probabilities = predict[0][top_10_indices]

    top_10_labels = label_encoder.inverse_transform(top_10_indices)
    ans = ''
    response = {'answer': ''}
    for label, probability in zip(top_10_labels, top_10_probabilities):
        s = label[0]
        for i in range(1, len(label)):
            if label[i].isupper():
                s += str(' / ') + label[i]
            else:
                s += label[i]
        ans += f'{s}: {probability * 100:.2f}%'+"\n"
    print(ans)
    response['answer'] = ans
    return response


if __name__ == '__main__':
    app.run(debug=True)
