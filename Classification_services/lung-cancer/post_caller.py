import requests
import json


with open("./sample_data/lung_cancer.json", "r") as file:
    data_dict = json.load(file)

url = 'http://127.0.0.1:5000/process'


data_to_send = data_dict

response = requests.post(url, json=data_to_send)

if response.status_code == 200:
    print('Request was successful.')
    print(f"You has a chances to be a lung cancer {response.json()['Cancer']} percent")
else:
    print('Request failed.')
    print('Status code:', response.status_code)