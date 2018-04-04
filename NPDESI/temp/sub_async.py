#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import netdev
import asyncio
import subprocess
from concurrent.futures import ProcessPoolExecutor

devices = [
    {
        'host': '10.10.30.4',
        'device_type': 'juniper_junos',
        'username': 'admin',
        'password': 'Juniper'
    },
    {
        'host': '10.10.30.5',
        'device_type': 'juniper_junos',
        'username': 'admin',
        'password': 'Juniper'
    }
]


def dump(hostname, data):
    with open('{}.cfg'.format(hostname), 'w') as f:
        f.write(data)


def ping(device):
    reply = subprocess.run(
        ['ping', '-c', '3', '-n', device['host']],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    if reply.returncode == 0:
        return True
    else:
        return False


def multi_conn(function, xdevices, limit=2):
    reachable_devices = []
    unreachable_devices = []

    with ProcessPoolExecutor(max_workers=limit) as executor:
        results = executor.map(function, xdevices)

        for device, is_reachable in zip(xdevices, results):
            if not is_reachable:
                print('{} is unreachable'.format(device['host']))
                unreachable_devices.append(device['host'])
            else:
                reachable_devices.append(device)

    return reachable_devices, unreachable_devices


async def task(param):
    async with netdev.create(**param) as con:
        output = await con.send_command('show configuration')
        return output

reachable_devices, unreachable_devices = multi_conn(ping, devices.copy())

if reachable_devices:
    loop = asyncio.get_event_loop()

    tasks = [
        loop.create_task(task(device))
        for device in reachable_devices
    ]

    loop.run_until_complete(asyncio.wait(tasks))

    for device, task in zip(reachable_devices, tasks):
        dump(device['host'], task.result())
    print('All reachable devices configs dumped')

else:
    print('No reachable devices devices')

if unreachable_devices:
    print("Unreachable devices are {}".format(', '.join(unreachable_devices)))
