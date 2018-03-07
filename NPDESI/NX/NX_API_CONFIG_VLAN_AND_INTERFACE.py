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

    commands = ['vlan 20', 'exit', 'interface Eth1/3', 'switchport', 'switchport access vlan 150']

    payload = {
        'ins_api': {
            'version': '1.0',
            'type': 'cli_conf',
            'chunk': '0',
            'sid': '1',
            'input': ' ; '.join(commands),
            'output_format': 'json'
        }
    }

    url = 'http://10.10.10.2/ins'

    responce = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)
    rx_object = json.loads(responce.text)
    print('Status code: ' + str(responce.status_code))

    print(json.dumps(rx_object, indent=4))
