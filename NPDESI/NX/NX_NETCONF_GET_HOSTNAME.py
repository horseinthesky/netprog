#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ncclient import manager

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
        <show>
            <hostname>
            </hostname>
        </show>
    """

    nc_get_reply = device.get(('subtree', get_filter))
    print(nc_get_reply.xml)
    ns_map = {'mod': 'http://www.cisco.com/nxos:1.0:vdc_mgr'}
    xml_rsp = nc_get_reply.data_ele.find('.//mod:hostname', ns_map)
    value = xml_rsp.text
    print(value)
