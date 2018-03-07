#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()

url = 'https://10.10.10.1/api/objects/networkobjects/web_server08'
auth = HTTPBasicAuth('cisco', 'cisco')

response = requests.delete(url, verify=False, auth=auth)
if response.status_code == 204:
    print('Status Code: ' + str(response.status_code))
    print('Object deleted')
else:
    print('ERROR Code: ' + str(response.status_code))
