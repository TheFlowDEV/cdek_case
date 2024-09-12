from flask import Flask, request, jsonify, render_template
import numpy as np
import json

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)

    return data


if __name__ == '__main__':
    app.run(debug=True)

