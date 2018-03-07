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
    rx_object = json.loads(response.text)
    static_routes = rx_object['ned:route']['ip-route-interface-forwarding-list']
    for route in static_routes:
        subnet = route['prefix']
        netmask = route['mask']
        next_hop = route['fwd-list'][0]['fwd']
        print('{}/{} via {}'.format(subnet, netmask, next_hop))
    # print(json.dumps(json.loads(response.text), indent=4))
