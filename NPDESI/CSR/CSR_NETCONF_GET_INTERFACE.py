#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lxml import etree
from ncclient import manager

host = '10.10.10.6'
port = 830
user = 'cisco'
pwd = 'cisco'


device = manager.connect(
    host=host,
    port=port,
    username=user,
    password=pwd,
    hostkey_verify=False,
    device_params={'name': 'csr'},
    allow_agent=False,
    look_for_keys=False
)

get_filter = """
            <native xmlns="http://cisco.com/ns/yang/ned/ios">
             <interface>
              <GigabitEthernet>
               <name>1</name>
              </GigabitEthernet>
             </interface>
            </native>
        """

nc_get_reply = device.get(('subtree', get_filter))
print(etree.tostring(nc_get_reply.data_ele, pretty_print=True).decode('ascii'))
