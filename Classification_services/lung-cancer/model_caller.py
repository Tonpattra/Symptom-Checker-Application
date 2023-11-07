import requests
from flask import Flask, jsonify, request
import pickle as pkl
from keras.models import load_model
import json
import numpy as np
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
model_cancer = load_model('./model/my_model.h5')

with open("./sample_data/lung_cancer.json", "r") as file:
    data_dict = json.load(file)

with open("./model/scaler-lung-cancer.pkl", "rb") as scal :
    scaler = pkl.load(scal)

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_request():
    data = request.get_json()
    data["Age"] = scaler.transform([[float(data["Age"])]])
    values = [float(value) for value in data.values()]
    numpy_array = np.array(values)
    # print(f"You has a chance to be lung cancer at {model_cancer.predict(numpy_array.reshape(1,-1)).item()*100:.2f} percent")
    response_data = {"Cancer": f"{model_cancer.predict(numpy_array.reshape(1,-1)).item()*100:.2f}"}

    return response_data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)