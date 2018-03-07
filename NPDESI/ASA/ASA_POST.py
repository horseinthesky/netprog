#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()

url = 'https://10.10.10.1/api/objects/networkobjects'
auth = HTTPBasicAuth('cisco', 'cisco')

payload = {
    "host": {
        "kind": "IPv4Address",
        "value": "10.10.10.118"
    },
    "kind": "object#NetworkObj",
    "name": "web_server08",
    "objectId": "web_server08"
}

headers = {'content-type': "application/json"}
response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False, auth=auth)
if response.status_code == 201:
    print('Status Code: ' + str(response.status_code))
    print(response.headers)
else:
    print('ERROR Code: ' + str(response.status_code))
    print(response.headers)
