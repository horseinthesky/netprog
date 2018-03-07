#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ncclient import manager

with manager.connect(
    host='10.10.10.4',
    port=22,
    username='cisco',
    password='cisco',
    device_params={'name': 'iosxr'},
    hostkey_verify=False,
    allow_agent=False, look_for_keys=False
) as device:
    nc_filter = """
        <config>
          <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
           <interface-configuration>
            <active>act</active>
              <interface-name>Loopback100</interface-name>
            <interface-virtual/>
           </interface-configuration>
          </interface-configurations>
        </config>
    """

    nc_reply = device.edit_config(target='candidate', config=nc_filter)
    device.commit()
