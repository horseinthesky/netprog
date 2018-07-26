#!/bin/env python3

import telnetlib
from time import sleep

host = '0.0.0.0'
port = 3517
timeout = 10


tn = telnetlib.Telnet(host, port, timeout)

try:
    tn.write('\r\n'.encode('ascii'))
    sleep(0.5)
    tn.write('root\n'.encode('ascii'))
    sleep(0.5)
    tn.write('cli\n'.encode('ascii'))
    sleep(0.5)
    tn.write('edit\n'.encode('ascii'))
    sleep(0.5)
    tn.write('set system services ssh\n'.encode('ascii'))
    sleep(0.5)
    tn.write('set system root-authentication plain-text-password\n'.encode('ascii'))
    sleep(0.5)
    tn.write('Juniper\n'.encode('ascii'))
    sleep(0.5)
    tn.write('Juniper\n'.encode('ascii'))
    sleep(0.5)
    tn.write('set system services netconf rfc-compliant ssh port 830\n'.encode('ascii'))
    sleep(0.5)
    tn.write('set interface em0 unit 0 family inet address 192.168.0.111/24\n'.encode('ascii'))
    sleep(0.5)
    tn.write('commit\n'.encode('ascii'))
    sleep(0.5)
    print(tn.read_very_eager().decode('ascii'))
except EOFError:
    pass
