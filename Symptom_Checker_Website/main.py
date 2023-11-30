from flask import Flask, render_template, request, redirect, jsonify
import pickle as pkl
import numpy as np
import json
import requests
from configuration import *
import warnings
import pandas as pd

warnings.filterwarnings("ignore")
question_lung = json.load(open('./data/lung_question.json', 'r'))
num_quest_lung = len(question_lung)
question_disease = json.load(open('./data/42_disease_question.json', 'r'))
num_quest_disease = len(question_disease)
loaded_data = pkl.load(open('./data/save_image_dict.pkl', 'rb'))
symptom = pkl.load(open('./data/symptom_name.pkl', 'rb'))
loaded_description = pd.read_csv('./data/symptom_Description.csv')
answers = {key: None for key in question_lung.keys()}
number_symp = len(symptom)
age = 'No'
gender = 'No'
web_app = Flask(__name__) 
web_app.config['GOOGLE_API_KEY'] = google_api
temp = {}

@web_app.route('/')
def home() :
    return render_template('homepage.html')

@web_app.route('/question_disease', methods=['GET', 'POST'])
def disease() :
    global temp
    first_time = request.form['first']

    if first_time == 'Yes' :
        with open("./data/reset_state.json", "r") as file: 
            data_json = json.load(file)
            
    else :
        data = f"""{{"current_node": {temp['current_node']},"answer": {request.form['response']}}}"""
        data_json = json.loads(data)
    url = f'http://{disease_host}:{disease_port}/decision_tree'
    response = requests.post(url, json=data_json)
    temp = response.json()
    try : 
        if int(temp['Question']) == 0 :
            responses = temp['Answer']  
            queue = loaded_data[responses][1]
            with open('static/images/suggest.jpg', 'wb') as f:
                f.write(queue)
            description = loaded_description[loaded_description.Disease == responses].Description.item()
            return render_template('information.html', disea = responses, drescript = description)
        else :    
            responses = temp['Question']
    except :
        responses = temp['Question']
    type_var = type(responses).__name__
    
    if type_var == "str" :
        question = f"Do you have {' '.join(responses.split('_'))}"

    else :
        question = f"Do you have one of these symptom \t ( {', '.join([' '.join(i.split('_')) for i in responses])} )"    


    return render_template('Question_disease.html' , 
                           prompt = question)

@web_app.route('/question_lung', methods=['GET', 'POST'])
def cancer():
    questions = list(question_lung.keys())
    if request.method == 'POST':
        current_index = int(request.form['index'])
        current_question = questions[current_index]
        answers[current_question] = request.form['answer']
        next_index = current_index + 1

        if next_index < len(questions):
            next_question = questions[next_index]
            return render_template('Question_lung.html', 
                                   prompt=question_lung[next_question],
                                   index=next_index)
        else:
            print(answers)
            response = requests.post(f'http://{lung_cancer_web}:{str(port_lung)}/process', json=answers)
            return render_template('result.html', percentag = response.json()['Cancer'])
    first_question = questions[0]
    return render_template('Question_lung.html', 
                           prompt=question_lung[first_question],
                           index=0)

@web_app.route('/find_hospital', methods=['GET', 'POST'])
def find_hospital() :
    return render_template('Nearby_hospital.html', google_api_key=web_app.config['GOOGLE_API_KEY'])

@web_app.route('/document', methods=['GET', 'POST'])
def knowledge() :
    if request.form['page'] == '1' :
        return render_template('document.html')
    else :
        return render_template('document.html')

if __name__ == '__main__':
    web_app.run(debug=True, host='0.0.0.0', port=port_website)