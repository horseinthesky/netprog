#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ncclient import manager

ios_xe1 = {
    'address': '10.10.30.6',
    'port': 830,
    'username': 'admin',
    'password': 'admin',
    'hostkey_verify': False
}


if __name__ == '__main__':
    with manager.connect(
        host=ios_xe1['address'],
        port=ios_xe1['port'],
        username=ios_xe1['username'],
        password=ios_xe1['password'],
        hostkey_verify=ios_xe1['hostkey_verify']
    ) as m:

        print("Here are the NETCONF Capabilities")
        for capability in m.server_capabilities:
            print(capability)
