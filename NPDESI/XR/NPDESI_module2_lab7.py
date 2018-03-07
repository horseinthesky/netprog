#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ncclient import manager

with manager.connect(
    host='10.10.10.4',
    port=22,
    username='cisco',
    password='cisco',
    device_params={'name': 'iosxr'},
    hostkey_verify=False,
    allow_agent=False, look_for_keys=False,
) as device:
    nc_filter = '''
        <config>
          <interface-configurations xmlns='http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg'>
            <interface-configuration>
              <active>act</active>
              <interface-name>Loopback100</interface-name>
              <interface-virtual/>
              <ipv4-network xmlns='http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-io-cfg'>
                <addresses>
                  <primary>
                    <address>100.100.1.1</address>
                    <netmask>255.255.255.0</netmask>
                  </primary>
                </addresses>
              </ipv4-network>
            </interface-configuration>
            <interface-configuration>
              <active>act</active>
              <interface-name>GigabitEthernet0/0/0/0</interface-name>
              <ipv4-network xmlns='http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-io-cfg'>
                <addresses>
                  <primary>
                    <address>10.23.23.1</address>
                    <netmask>255.255.255.0</netmask>
                  </primary>
                  <secondaries>
                    <secondary>
                      <address>20.23.23.1</address>
                      <netmask>255.255.255.0</netmask>
                    </secondary>
                  </secondaries>
                </addresses>
              </ipv4-network>
            </interface-configuration>
            <interface-configuration>
              <active>act</active>
              <interface-name>GigabitEthernet0/0/0/0.10</interface-name>
              <interface-mode-non-physical>default</interface-mode-non-physical>
              <description>TEST_SUBINTERFACE</description>
              <ipv4-network xmlns='http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-io-cfg'>
                <addresses>
                  <primary>
                    <address>20.10.10.1</address>
                    <netmask>255.255.255.0</netmask>
                  </primary>
                </addresses>
              </ipv4-network>
            </interface-configuration>
          </interface-configurations>
        </config>
    '''

    nc_reply = device.edit_config(target='candidate', config=nc_filter)
    print(nc_reply)
    device.commit()
