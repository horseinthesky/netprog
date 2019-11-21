#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

INVENTORY_FILE = 'inventory.yml'

for region in inventory['regions']:
    for 
def read_yaml(file_name=INVENTORY_FILE):
    with open(file_name) as f:
        result = yaml.load(f)
    return result

def main():
    devices_variables = read_yaml(INVENTORY_FILE)
    for rr in rrs_list:
        params = GLOBAL_DEVICE_PARAMS.copy()
        params['host'] = juniper_mx_ip
        configure_device(params, devices_variables)

if __name__ == '__main__':
    main()
