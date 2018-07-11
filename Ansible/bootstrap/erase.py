#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from telnetlib import Telnet
from concurrent.futures import ProcessPoolExecutor
from copy import deepcopy

eve_ip = '192.168.0.11'

devices = [
    {'hostname': 'CE1', 'port': '32769', 'ip': '192.168.0.201'},
    {'hostname': 'CE2', 'port': '32770', 'ip': '192.168.0.202'},
    {'hostname': 'PE1', 'port': '32771', 'ip': '192.168.0.203'},
    {'hostname': 'PE2', 'port': '32772', 'ip': '192.168.0.204'},
    {'hostname': 'P', 'port': '32773', 'ip': '192.168.0.205'},
]


def setup(device_dict):
    port = device_dict['port']
    tn = Telnet(eve_ip, port)
    tn.write(('\r\n').encode('ascii'))
    tn.write(('erase startup-config\n').encode('ascii'))
    tn.write(('\r\n').encode('ascii'))
    time.sleep(3)
    tn.write(('reload\n').encode('ascii'))
    tn.write(('no\n').encode('ascii'))
    time.sleep(1)
    tn.write(('\r\n').encode('ascii'))


def multi_conn(function, devices, limit=14):
    with ProcessPoolExecutor(max_workers=limit) as executor:
        executor.map(function, devices)


if __name__ == '__main__':
    multi_conn(setup, devices)
    print('All done')
