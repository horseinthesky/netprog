#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from ncclient import manager
import sys


# the variables below assume the user is requesting access to a
# device running in VIRL
# use the IP address or hostname of your device
HOST = '10.10.10.3'
# use the NETCONF port for your Nexus device
PORT = 22
# use the user credentials for your Nexus device
USER = 'cisco'
PASS = 'cisco'


# create a main() method
def main():
    logging.basicConfig(level=logging.DEBUG)
    """Main method that prints NETCONF capabilities of remote device."""
    with manager.connect(host=HOST, port=PORT, username=USER, password=PASS,
                         hostkey_verify=False, device_params={'name': 'csr'},
                         look_for_keys=False, allow_agent=False) as m:

        # print all NETCONF capabilities
        print('***Here are the Remote Devices Capabilities***')
        for capability in m.server_capabilities:
            print(capability)


if __name__ == '__main__':
    sys.exit(main())
