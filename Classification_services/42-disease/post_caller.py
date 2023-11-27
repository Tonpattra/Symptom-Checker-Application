import requests
import json

# with open("./sample_data/reset_state.json", "r") as file:
#     data_dict = json.load(file)

with open("./sample_data/next_state.json", "r") as file: #for next state request
    data_dict = json.load(file)

url = 'http://127.0.0.1:8080/decision_tree'
data_to_send = data_dict
response = requests.post(url, json=data_to_send)

if response.status_code == 200:
    print('Request was successful.')
    print(f"{response.json()}")
else:
    print('Request failed.')
    print('Status code:', response.status_code)