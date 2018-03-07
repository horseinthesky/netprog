#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()

if __name__ == "__main__":

    auth = HTTPBasicAuth('cisco', 'cisco')
    headers = {'Accept': 'application/vnd.yang.data+json'}
    url = 'http://10.10.10.6/restconf/api/config/native/ip/route?deep'
    response = requests.get(url, verify=False, headers=headers, auth=auth)
    print(json.dumps(json.loads(response.text), indent=4))
