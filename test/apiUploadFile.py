import requests
import json
#from .apiLogin import login

url = 'http://localhost:5000/api/v1'

def uploadFile(url, token, file, file_desc):
    
    url   = url

    headers = {'Authorization':'Bearer '+token}    
    #data = {'file_description':file_desc}
    files = {'file':file}
    #files = {'file':file}
    
    #resp = requests.post(url, headers=headers, files=files, data=data)
    resp = requests.post(url, headers=headers, files=files)

    return resp.json()

if __name__ == "__main__":
    
    turl = url +'/contents/video'
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NDE1NDAxNTUsIm5iZiI6MTY0MTU0MDE1NSwianRpIjoiZGQ4MTU1NTAtYTA4MS00YTNkLTg1ZTEtODM3ZmQ1MzJkYjA2IiwiZXhwIjoxNjQxNTQxMDU1LCJpZGVudGl0eSI6MSwiZnJlc2giOnRydWUsInR5cGUiOiJhY2Nlc3MifQ.YwXw3rc0vbsNE4MPom7641_axfwH1iCmz6htv5bkvpA'
    file = open('C:\\pjt\\file_example.mp4', 'rb')
    file_desc = 'TEST file'
    
    rtn = uploadFile(turl, token, file, file_desc)
    print(rtn)