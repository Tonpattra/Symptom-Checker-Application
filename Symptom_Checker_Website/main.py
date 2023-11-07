from flask import Flask, render_template, request, redirect, jsonify
import pickle as pkl
import numpy as np
import json
import requests

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
web_app.config['GOOGLE_API_KEY'] = 'wait_for_API_complete ja'


@web_app.route('/')
def home() :
    return render_template('home.html')

# @web_app.route('/result')
# def result() : 
#     user_input = request.args.get('user_input') 
#     return f"This is the result page. User input: {user_input}"

@web_app.route('/question_disease', methods=['GET', 'POST'])
def question_diseas() :

    ran = np.random.randint(0, num_quest_disease)
    question_a = question_disease[list(question_disease.items())[ran][0]]
    random_symp = question_a
    age = 'No'
    gender = 'No'

    return render_template('questionaire.html' , 
                           quest = random_symp,
                           gender = gender,
                           age = age)

@web_app.route('/find_hospital', methods=['GET', 'POST'])
def find_hos() :
    return render_template('hospital.html', google_api_key=web_app.config['GOOGLE_API_KEY'])

@web_app.route('/web_test', methods=['GET', 'POST'])
def survey():
    questions = list(question_lung.keys())
    
    if request.method == 'POST':

        current_index = int(request.form['index'])
        current_question = questions[current_index]

        answers[current_question] = request.form['answer']

        next_index = current_index + 1
        if next_index < len(questions):
            next_question = questions[next_index]
            return render_template('survey.html', 
                                   prompt=question_lung[next_question],
                                   index=next_index)
        else:
            print(answers)
            response = requests.post('http://lung-cancer-services:5000/process', json=answers)
            return f"<h3>You has a chances to be a lung cancer {response.json()['Cancer']} percent</h3>"

    first_question = questions[0]
    return render_template('survey.html', 
                           prompt=question_lung[first_question],
                           index=0)

if __name__ == '__main__':
    web_app.run(debug=False, host='0.0.0.0', port=800)