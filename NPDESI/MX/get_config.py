#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from requests.auth import HTTPBasicAuth

if __name__ == "__main__":

    auth = HTTPBasicAuth('admin', 'Juniper')
    headers = {'Accept': 'application/json'}
    url = 'http://192.168.0.110:8080/rpc/get-configuration'
    response = requests.get(url, verify=False, headers=headers, auth=auth)
    print(json.dumps(json.loads(response.text), indent=4))
