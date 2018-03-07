#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
requests.packages.urllib3.disable_warnings()

url = "https://192.168.0.10/api/v1/policy"

headers = {
    'x-auth-token': "ST-8-0djEFSyeErcCYiBcvSAd-cas",
    'cache-control': "no-cache",
    'postman-token': "893f46c0-7c54-7b9f-c87d-bef6c6c38ca1"
}

response = requests.request("GET", url, headers=headers, verify=False)

# print(response.text)
output = json.loads(response.text)
print(json.dumps(output, indent=4))
