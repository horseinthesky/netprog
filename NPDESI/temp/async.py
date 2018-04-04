#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import netdev
import asyncio

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


async def task(param):
    async with netdev.create(**param) as con:
        output = await con.send_command('show configuration')
        return output


loop = asyncio.get_event_loop()
tasks = [
    loop.create_task(task(device))
    for device in devices
]
loop.run_until_complete(asyncio.wait(tasks))
for task in tasks:
    print(task.result())
