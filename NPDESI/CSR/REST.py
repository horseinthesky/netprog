#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from requests.auth import HTTPBasicAuth

if __name__ == "__main__":

    auth = HTTPBasicAuth('cisco', 'cisco')
    headers = {'Accept': 'application/json'}
    url = "http://10.10.10.3/api/config/interfaces"
    response = requests.get(url, verify=False, headers=headers, auth=auth)
    print(response.status_code)
    print(response.text)
