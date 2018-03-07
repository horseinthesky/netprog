#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ncclient import manager
from lxml import etree

with manager.connect(
    host='10.10.10.5',
    port=22,
    username='cisco',
    password='cisco',
    device_params={'name': 'nexus'},
    hostkey_verify=False,
    allow_agent=False,
    look_for_keys=False
) as device:

    get_filter = """
        <show xmlns="http://www.cisco.com/nxos:1.0">
            <vlan>
            </vlan>
        </show>
    """
    nc_get_reply = device.get(('subtree', get_filter))
    print(etree.tostring(nc_get_reply.data_ele, pretty_print=True).decode('ascii'))
