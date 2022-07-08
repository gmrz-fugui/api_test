import requests
import json
import logging

def post():

    url='http://192.168.3.203:8080/uaf/device/list'
    header = {
        "Content-Type": "application/fido+uaf"
    }
    data={
        "context":{
            "appID":1103,
            "transNo":"test-66666666666",
            "userName":"gmrzFff51674441911639122468"
        }
    }
    try:
        r= requests.post(url,  headers=header,data=json.dumps(data))
        return r.json()
    except Exception as e:
        return e

print(post())
