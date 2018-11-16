#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ncclient import manager
from getpass import getuser
import xmltodict
import json
# import logging
# import sys
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(levelname)s: %(message)s',
#                     stream=sys.stdout)

intf_rpc = "<get-interface-information format='xml'><terse/></get-interface-information>"
bgp_nei_rpc = '<get-bgp-neighbor-information/>'

m = manager.connect(
    host='10.10.10.7',
    port=22,
    username='juniper',
    password='Juniper!',
    hostkey_verify=False,
    device_params={'name': 'junos'}
)

response = m.rpc(intf_rpc)
output_data = json.dumps(xmltodict.parse(response.data_xml))
print(output_data)
