#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netmiko import ConnectHandler
from concurrent.futures import ProcessPoolExecutor

devices = [
    {
        'ip': '10.10.30.4',
        'device_type': 'juniper_junos',
        'username': 'admin',
        'password': 'Juniper'
    },
    {
        'ip': '10.10.30.5',
        'device_type': 'juniper_junos',
        'username': 'admin',
        'password': 'Juniper'
    }
]


def send_command(device_params, command='show configuration'):
    with ConnectHandler(**device_params) as ssh:
        device_result = ssh.send_command(command)
    print(device_result)


def multi_conn(function, devices, limit=2):
    with ProcessPoolExecutor(max_workers=limit) as executor:
        executor.map(function, devices)


if __name__ == '__main__':
    multi_conn(send_command, devices)
