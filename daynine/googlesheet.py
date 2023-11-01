import requests
from datetime import datetime
import json
import os
from dotenv import load_dotenv
load_dotenv()


APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")

# get excercise query
queryPath = "daynine/queryResponse.json"
def postExcercise(endpoint,token,param):
    response = requests.post(url=endpoint,headers=token,json=param)
    response = response.json()
    print(response)
    try:
        with open(queryPath,"r") as read_file:
            query_data = json.load(read_file)
            query_data['exercises'].extend(response['exercises'])
        
        with open(queryPath,"w+") as write_file:
            json.dump(query_data,write_file,indent=4)

    except FileNotFoundError:
        with open(queryPath,"w") as open_file:
            json.dump(response,open_file,indent=4)
    return response

url = "https://trackapi.nutritionix.com/v2/natural/exercise"

queryHeaders = {
    "x-app-id" : APP_ID,
    "x-app-key" : APP_KEY}

runQuery = input("what you did ? ")

queryParam = {
    "query": runQuery
}


content = postExcercise(url,queryHeaders,queryParam)
print(json.dumps(content,indent=4))

def colValues(content):
    today_date = datetime.now().strftime("%m/%d/%y")
    cr_time = datetime.now().strftime("%H:%M:%S")
    col_data = [today_date,cr_time]
    for i in range(len(content["exercises"])):
        temp = []
        temp.append(content["exercises"][i]["name"])
        temp.append(content["exercises"][i]["duration_min"])
        temp.append(content["exercises"][i]["nf_calories"])
        col_data.append(temp)
    return col_data

body_data = colValues(content)

row_url = "https://api.sheety.co/d505e4aa374085caa6ccc710947acf9f/myWorkouts/workouts"
row_header = {
    'Authorization': os.getenv("AUTH"),
    'Content-Type': 'application/json'
}

def addRow(url,token):
    for i in range(2,len(body_data)):
        body = {
        "workout" : {
        "date": body_data[0],
        "time":body_data[1],
        "exercise": body_data[i][0],
        "duration": body_data[i][1],
        "calories":body_data[i][2]
            }
        }

        response = requests.post(url=url,headers=token,data = json.dumps(body))
        print(response.status_code)
        print(response.json())

addRow(row_url,row_header)






