#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ncclient import manager
from pprint import pprint
import xmltodict

ios_xe1 = {
    'address': '192.168.0.203',
    'port': 830,
    'username': 'admin',
    'password': 'admin',
}


if __name__ == '__main__':
    with manager.connect(host=ios_xe1['address'], port=ios_xe1['port'],
                         username=ios_xe1['username'],
                         password=ios_xe1['password'],
                         hostkey_verify=False) as m:

        netconf_reply = m.get_config(source='running')
        pprint(netconf_reply)
