#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from requests.auth import HTTPBasicAuth

headers = {'Content-Type': 'application/xml'}

auth = HTTPBasicAuth('admin', 'Juniper')

url = 'http://192.168.0.110:8080/rpc'

data = '''
    <lock-configuration/>
    <edit-config>
        <target>
            <candidate />
        </target>
        <config>
            <configuration>
                <system>
                    <host-name>TEST_HOSTNAME</host-name>
                </system>
            </configuration>
        </config>
    </edit-config>
    <commit/>
    <unlock-configuration/>
'''

if __name__ == "__main__":
    response = requests.post(url, data=data, headers=headers, auth=auth)
    print(response.status_code)
