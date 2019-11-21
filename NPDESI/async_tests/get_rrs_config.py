#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import asyncio
import netdev

INVENTORY_FILE = 'netmap.yaml'
PARAMS = {'username': 'admin', 'password': 'Juniper', 'device_type': 'juniper_junos'}
COMMAND = 'show configuration'


def get_devices_params(file_name=INVENTORY_FILE):
    with open(file_name) as f:
        inventory = yaml.load(f)
        devices_list = []
        fvrrs = []
        vpn_rrs = []
        for region in inventory['regions']:
            fvrrs.extend(inventory['regions'][region]['external_rrs'])
            for device in fvrrs:
                device.update(PARAMS)
                device.update({'host': device['mgmt_ip']})
                del(device['hostname'])
                del(device['model'])
                del(device['lo0_ip'])
                del(device['mgmt_ip'])
                del(device['server'])
                del(device['type'])
            devices_list.extend(fvrrs)
            for data_center in inventory['regions'][region]['data_centers']:
                for building in inventory['regions'][region]['data_centers'][data_center]['buildings']:
                    for module in inventory['regions'][region]['data_centers'][data_center]['buildings'][building]['modules']:
                        if 'vpn_rrs' in inventory['regions'][region]['data_centers'][data_center]['buildings'][building]['modules'][module].keys():
                            vpn_rrs.extend(inventory['regions'][region]['data_centers'][data_center]['buildings'][building]['modules'][module]['vpn_rrs'])
                            for device in vpn_rrs:
                                device.update(PARAMS)
                                device.update({'host': device['mgmt_ip']})
                                del(device['hostname'])
                                del(device['model'])
                                del(device['lo0_ip'])
                                del(device['mgmt_ip'])
                            devices_list.extend(vpn_rrs)
    print(devices_list)
    return devices_list


async def collect_outputs(device_params, command):
    # hostname = device_params.pop('hostname')
    async with netdev.create(**device_params) as connection:
        command_result = await connection.send_command(command)
        return command_result


def main():
    inventory = get_devices_params(INVENTORY_FILE)
    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(collect_outputs(device, COMMAND))
        for device in inventory
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    for task in tasks:
        print(task.result())


if __name__ == '__main__':
    main()
