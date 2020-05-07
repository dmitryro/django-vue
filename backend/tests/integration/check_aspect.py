import json
import os
import requests


def get_bearer_token(username, password):
     """
     Get the bearer tocken from username and password
     """
     headers = {}
     headers["Content-Type"] = "application/json"
    
     data = {}
     data['username'] = username
     data['password'] = password
     url = 'http://0.0.0.0:80/api-token-auth/'
     r = requests.post(url=url, headers=headers, data=json.dumps(data))
     return r.get('token', None)


def test_ascpect_ratio():
     """
     Test aspect ration
     """
     url = ''
     headers = {}
     username = os.environ["USERNAME"]
     password = os.environ["PASSWORD"]
     token = get_bearer_token(username, password)
     headers["Content-Type"] = "application/json"
     headers["Authorization"] = f"Bearer {token}" 
     r = requests.get(url=url, headers=headers)
     print(r)





 
