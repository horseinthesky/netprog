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
            'input': 'show interface mgmt 0',
            'output_format': 'json'
        }
    }

    url = 'http://10.10.10.2/ins'

    responce = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)
    rx_object = json.loads(responce.text)
    print('Status code: ' + str(responce.status_code))
    interface_data = rx_object['ins_api']['outputs']['output']['body']['TABLE_interface']['ROW_interface']
    ip_address = interface_data['eth_ip_addr']
    netmask = interface_data['eth_ip_mask']
    speed = interface_data['eth_speed']
    state = interface_data['state']
    MTU = interface_data['eth_mtu']
    print('Management Interface Information:')
    print('{:15}{}/{}'.format('IP Address:', ip_address, netmask))
    print('{:15}{}'.format('Speed:', speed))
    print('{:15}{}'.format('State:', state))
    print('{:15}{}'.format('MTU:', MTU))
