from flask import Flask, render_template, request, redirect, jsonify
import pickle as pkl
import numpy as np
import json
import requests
from configuration import *
import warnings


warnings.filterwarnings("ignore")
question_lung = json.load(open('./data/lung_question.json', 'r'))
num_quest_lung = len(question_lung)
question_disease = json.load(open('./data/42_disease_question.json', 'r'))
num_quest_disease = len(question_disease)
symptom = pkl.load(open('./data/symptom_name.pkl', 'rb'))
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
    yes_count = 0
    mean = 0
    sum = 0
    try :
        yes_count = 0
        sum = 0
        for key, value in request.form.items():
            if key.startswith('response') :
                sum += 1
                if  value == '1':
                    yes_count += 1
        mean = yes_count/sum             
    except :
        pass            

    if first_time == 'Yes' :
        with open("./data/reset_state.json", "r") as file: #for next state request
            data_json = json.load(file)
    else :
        data = f"""{{"current_node": {temp['current_node']},"answer": {int(mean)}}}"""
        data_json = json.loads(data)

    url = f'http://{disease_host}:{disease_port}/decision_tree'
    response = requests.post(url, json=data_json)
    temp = response.json()
    try : 
        if int(temp['Question']) == 0 :
            responses = temp['Answer']  
            return f"<h3>You has a {responses} </h3>"
        else :    
            responses = temp['Question']
    except :
        responses = temp['Question']
    type_var = type(responses).__name__

    return render_template('questionaire.html' , 
                           quest = responses,
                           type_variable = type_var)

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
            return render_template('Question.html', 
                                   prompt=question_lung[next_question],
                                   index=next_index)
        else:
            print(answers)
            response = requests.post(f'http://{lung_cancer_web}:{str(port_lung)}/process', json=answers)
            return render_template('result.html', percentag = response.json()['Cancer'])
            # return f"<h3>You has a chances to be a lung cancer {response.json()['Cancer']} percent</h3>"
    first_question = questions[0]
    return render_template('Question.html', 
                           prompt=question_lung[first_question],
                           index=0)

@web_app.route('/find_hospital', methods=['GET', 'POST'])
def find_hospital() :
    return render_template('hospital.html', google_api_key=web_app.config['GOOGLE_API_KEY'])

if __name__ == '__main__':
    web_app.run(debug=True, host='0.0.0.0', port=port_website)