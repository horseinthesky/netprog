#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lxml import etree
from ncclient import manager

host = '10.10.10.6'
port = 830
user = 'cisco'
pwd = 'cisco'

with manager.connect(
    host=host,
    port=port,
    username=user,
    password=pwd,
    hostkey_verify=False,
    device_params={'name': 'csr'},
    allow_agent=False,
    look_for_keys=False
) as device:

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
    x = etree.tostring(nc_get_reply.data_ele).decode('ascii')
    y = etree.fromstring(x)
    interface = y.find('.//{http://cisco.com/ns/yang/ned/ios}name').text
    description = y.find('.//{http://cisco.com/ns/yang/ned/ios}description').text
    address = nc_get_reply.data_ele[0][0][0][3][0][0][0].text
    # address = y.find('.//{http://cisco.com/ns/yang/ned/ios}address').text
    mask = y.find('.//{http://cisco.com/ns/yang/ned/ios}mask').text
    print('{:18} {:18} {:18} {:18}'.format('Interface', 'Address', 'Mask', 'Description'))
    print('{:18} {:18} {:18} {:18}'.format('GigabitEthernet' + interface, address, mask, description))
