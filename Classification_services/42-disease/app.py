import requests
from flask import Flask, jsonify, request
import pickle
import json
import numpy as np
import os
import random
import warnings

warnings.filterwarnings("ignore")

with open("models/disease_predictor.pkl", 'rb') as f :
    clf = pickle.load(f)

with open("models/label_encoder.pkl",'rb') as f :
    label_encoder = pickle.load(f) 

with open("models/tags_symptoms.pkl",'rb') as f :
    tags_symptoms = pickle.load(f)    

app = Flask(__name__)

@app.route('/decision_tree', methods=['POST'])
def decision_tree_request():
    # input ={current_node:"reset"(for start), answer:{0,1}} 
    data = request.get_json()

    # for begin
    if data["current_node"] == "reset":
        current_node = 0 
        feature = clf.feature_names_in_[clf.tree_.feature[current_node]]
        response_data = {"Question": str(feature),"current_node":int(current_node),"Answer":int(0)}
        return response_data

    current_node = data["current_node"]
    threshold = clf.tree_.threshold[current_node]

    # Check the condition based on the user input and the threshold
    if data["answer"] <= threshold:
        current_node = clf.tree_.children_left[current_node]

    else:
        current_node = clf.tree_.children_right[current_node]

    feature = clf.tree_.feature[current_node]
    
    
    if feature <0:  # Reached a leaf node
        predicted_value = clf.tree_.value[current_node]
        final_prediction = label_encoder.inverse_transform([predicted_value.argmax()])[0]

        response_data = {"Question": int(0),"current_node":int(current_node),"Answer":str(final_prediction)}
        return response_data
    
    else: 
        feature_name = clf.feature_names_in_[feature]
        if feature_name[:3]=="sym":
            feature_name = tags_symptoms[feature_name]

        response_data = {"Question": feature_name,"current_node":int(current_node),"Answer":int(0)}
        return response_data


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)