#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ncclient import manager
from pprint import pprint
import xmltodict

ios_xe1 = {
    'address': '10.10.30.4',
    'port': 830,
    'username': 'root',
    'password': 'Juniper',
}

# NETCONF filter to use
netconf_filter = open("filter-ietf-interfaces.xml").read()

if __name__ == '__main__':
    with manager.connect(host=ios_xe1['address'], port=ios_xe1['port'],
                         username=ios_xe1['username'],
                         password=ios_xe1['password'],
                         hostkey_verify=False) as m:

        # Get Configuration and State Info for Interface
        netconf_reply = m.get_config(source='running')
        pprint(netconf_reply)

        # Process the XML and store in useful dictionaries
        # intf_details = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]
        # intf_config = intf_details["interfaces"]["interface"]

        # print("")
        # print("Interface Details:")
        # print("  Name: {}".format(intf_config["name"]))
        # print("  Description: {}".format(intf_config["description"]))
        # print("  Type: {}".format(intf_config["type"]["#text"]))
        # print("  Address: {}".format(intf_config["ipv4"]["address"]["ip"]))
        # print("  Netmask: {}".format(intf_config["ipv4"]["address"]["netmask"]))
