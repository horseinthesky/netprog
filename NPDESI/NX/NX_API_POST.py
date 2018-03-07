#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from requests.auth import HTTPBasicAuth

if __name__ == "__main__":

    auth = HTTPBasicAuth('cisco', 'cisco')
    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        "ins_api": {
            "version": "1.0",
            "type": "cli_show",
            "chunk": "0",
            "sid": "1",
            "input": "show clock",
            "output_format": "json"
        }
    }

url = 'http://10.10.10.2/ins'

response = requests.post(url, data=json.dumps(payload),
                         headers=headers, auth=auth)

print('Status Code: ' + str(response.status_code))
rx_object = json.loads(response.text)
print(json.dumps(rx_object, indent=4))
