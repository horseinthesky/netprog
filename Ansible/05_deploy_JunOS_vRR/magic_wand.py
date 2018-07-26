#!/bin/env python

host = '0.0.0.0'
port = 3517
timeout = 10

import telnetlib

tn = telnetlib.Telnet(host, port, timeout)

try:
    tn.write('\r\n')
except EOFError:
    pass
