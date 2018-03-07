#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import requests
import json
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()


class TestDeviceConfiguration(unittest.TestCase):

    def test_npdesi_snmp_ro(self):
        """Validate npdesi is a configured RO string
        """
        auth = HTTPBasicAuth('cisco', 'cisco')
        headers = {'Accept': 'application/vnd.yang.data+json'}
        url = 'http://10.10.10.6/restconf/api/config/native/snmp-server?deep'
        response = requests.get(url, verify=False, headers=headers, auth=auth)

        parse = json.loads(response.text)
        community_list = parse['ned:snmp-server']['community']
        expected = {'name': 'npdesi', 'RO': [None]}
        is_there = expected in community_list
        self.assertTrue(is_there)

    def test_cisco_snmp_ro(self):
        """Validate cisco is a configured RO string
        """
        auth = HTTPBasicAuth('cisco', 'cisco')
        headers = {'Accept': 'application/vnd.yang.data+json'}
        url = 'http://10.10.10.6/restconf/api/config/native/snmp-server?deep'
        response = requests.get(url, verify=False, headers=headers, auth=auth)

        parse = json.loads(response.text)
        community_list = parse['ned:snmp-server']['community']
        expected = {'name': 'cisco', 'RO': [None]}
        is_there = expected in community_list
        self.assertTrue(is_there)

    def test_cisco_secure_snmp_rw(self):
        """Validate cisco_secure is a configured RW string
        """
        auth = HTTPBasicAuth('cisco', 'cisco')
        headers = {'Accept': 'application/vnd.yang.data+json'}
        url = 'http://10.10.10.6/restconf/api/config/native/snmp-server?deep'
        response = requests.get(url, verify=False, headers=headers, auth=auth)

        parse = json.loads(response.text)
        community_list = parse['ned:snmp-server']['community']
        expected = {'name': 'cisco_secure', 'RW': [None]}
        is_there = expected in community_list
        self.assertTrue(is_there)

    def test_devops_user_exists(self):
        """Validate devops user exist on the device
        """
        auth = HTTPBasicAuth('cisco', 'cisco')
        headers = {'Accept': 'application/vnd.yang.collection+json'}
        url = 'http://10.10.10.6/restconf/api/config/native/username'
        response = requests.get(url, verify=False, headers=headers, auth=auth)

        parse = json.loads(response.text)
        users_list = parse['collection']['ned:username']
        expected = 'devops'
        is_there = False
        for user in users_list:
            if expected in user['name']:
                is_there = True
        self.assertTrue(is_there)

    def test_super_user_user_exists(self):
        """Validate devops user exist on the device
        """
        auth = HTTPBasicAuth('cisco', 'cisco')
        headers = {'Accept': 'application/vnd.yang.collection+json'}
        url = 'http://10.10.10.6/restconf/api/config/native/username'
        response = requests.get(url, verify=False, headers=headers, auth=auth)

        parse = json.loads(response.text)
        users_list = parse['collection']['ned:username']
        expected = 'super_user'
        is_there = False
        for user in users_list:
            if expected in user['name']:
                is_there = True
        self.assertTrue(is_there)


if __name__ == "__main__":
    unittest.main()
