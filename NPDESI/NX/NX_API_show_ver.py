#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from requests.auth import HTTPBasicAuth

if __name__ == '__main__':
    auth = HTTPBasicAuth('cisco', 'cisco')
    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        'ins_api': {
            'version': '1.0',
            'type': 'cli_show',
            'chunk': '0',
            'sid': '1',
            'input': 'show version',
            'output_format': 'json'
        }
    }

    url = 'http://10.10.10.2/ins'

    responce = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)
    rx_object = json.loads(responce.text)
    os_version = rx_object['ins_api']['outputs']['output']['body']['kickstart_ver_str']
    print('Status code: ' + str(responce.status_code))
    print('OS: ', os_version)
