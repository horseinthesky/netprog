#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import yaml
from requests.auth import HTTPBasicAuth

if __name__ == "__main__":

    auth = HTTPBasicAuth('admin', 'Juniper')
    headers = {'Accept': 'application/json'}
    url = 'http://192.168.0.110:8080/rpc/get-configuration'
    response = requests.get(url, headers=headers, auth=auth)
    with open('vrr.yml', 'w') as cfg:
        yaml.dump(json.loads(response.text), cfg)
