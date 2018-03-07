#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()

url = 'https://10.10.10.1/api/monitoring/device/components/version'
auth = HTTPBasicAuth('cisco', 'cisco')

response = requests.get(url, verify=False, auth=auth)

if response.status_code == 200:
    print('Status Code: ' + str(response.status_code))
    parse = json.loads(response.text)
    print(json.dumps(parse, indent=4))
else:
    print('ERROR Code: ' + str(response.status_code))
