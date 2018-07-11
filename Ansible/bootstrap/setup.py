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

commands = [
    'enable',
    'conf t',
    'line con 0',
    'exec-timeout 0 0',
    'privilege level 15',
    'logging synchronous',
    'transport output none',
    'exit',
    'line vty 0 4',
    'exec-timeout 0 0',
    'privilege level 15',
    'logging synchronous',
    'transport output none',
    'login local',
    'exit',
    'no service config',
    'no ip tftp source-interface GigabitEthernet4',
    'username admin privilege 15 password admin',
    'ip domain-name lab.local',
    'crypto key generate rsa modulus 1024',
    'ip vrf MGMT',
    'exit'
]


def setup(device_dict):
    hostname, port, ip = device_dict['hostname'], device_dict['port'], device_dict['ip']
    tn = Telnet(eve_ip, port)
    device_commands = deepcopy(commands)
    device_commands.insert(2, 'hostname {}'.format(hostname))
    device_commands.extend(['interface Gi4', 'ip vrf forwarding MGMT', 'ip address {} 255.255.255.0'.format(ip), 'exit'])
    tn.write(('\r\n').encode('ascii'))
    for command in device_commands:
        tn.write((command + '\n').encode('ascii'))
        if ('address' or 'crypto') in command:
            time.sleep(7)
    tn.write(('netconf-yang\n').encode('ascii'))
    time.sleep(4)
    tn.write(('exit\n').encode('ascii'))
    tn.write(('write\n').encode('ascii'))


def multi_conn(function, devices, limit=14):
    with ProcessPoolExecutor(max_workers=limit) as executor:
        executor.map(function, devices)


if __name__ == '__main__':
    multi_conn(setup, devices)
    print('All done')
