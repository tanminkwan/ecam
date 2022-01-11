import requests
import json

def login(url, id, pw):
    
    data = dict(password=pw, username=id, provider='db', refresh='true')
    headers = {'Content-Type':'application/json'} 
    resp = requests.post(url, data=json.dumps(data), headers=headers)

    print('resp header : ',resp.headers)
    print('Result : ',resp.json())
    
    return resp.json()['access_token']


if __name__ == "__main__":
    
    token = login('http://localhost:5000/api/v1/security/login','tiffanie','1q2w3e4r!!')
    print(token)