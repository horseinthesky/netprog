#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ncclient import manager

with manager.connect(
    host='10.10.10.8',
    port=22,
    username='root',
    password='Juniper',
    device_params={'name': 'junos'},
    hostkey_verify=False,
    allow_agent=False, look_for_keys=False
) as device:
    nc_get_reply = device.get_config(source='running')
    print(nc_get_reply)
