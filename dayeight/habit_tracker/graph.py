import requests
from datetime import datetime
user_create = "https://pixe.la/v1/users"
TOKEN = "typomista56dsf5df5ke89"
username = "yogendra1324"

user_param = {
    "token":TOKEN,
    "username":username,
    "agreeTermsOfService" : "yes",
    "notMinor":"yes"
}

graph_endpoint = "https://pixe.la/v1/users/yogendra1324/graphs"

graph_params = {
    "id" : "codegraph1",
    "name": "codeRepo",
    "unit":"commit",
    "type":"int",
    "color":"ajisai"
    }

login_headers = {
    "X-USER-TOKEN":TOKEN
}

codePixel = "https://pixe.la/v1/users/yogendra1324/graphs/codegraph1"



pixel_params = {
    "date": "20231028",
    "quantity":"30"
}

def postActions(endpoints,params,header):
    response = requests.post(url=endpoints,json=params,headers=header)
    print(response.text)


# def putActions

# postActions(codePixel,pixel_params,login_headers)
putPixel = "https://pixe.la/v1/users/yogendra1324/graphs/codegraph1/20231028"


putParams = {
    "quantity":"0"
}

def putAction(endpoints,params,header):
    reposnse = requests.put(url=endpoints,json=params,headers=header)
    print(reposnse.text)


putAction(putPixel,putParams,login_headers)