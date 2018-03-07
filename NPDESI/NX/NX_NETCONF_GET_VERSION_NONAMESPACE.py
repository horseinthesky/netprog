#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ncclient import manager


def remove_namespaces(xml):
        for elem in xml.getiterator():
            split_tag = elem.tag.split('}')
            if len(split_tag) > 1:
                elem.tag = split_tag[1]
        return xml


with manager.connect(
    host='10.10.10.5',
    port=22,
    username='cisco',
    password='cisco',
    device_params={'name': 'nexus'},
    hostkey_verify=False,
    allow_agent=False,
    look_for_keys=False
) as device:

    get_filter = """
        <show>
            <version>
            </version>
        </show>
    """

    nc_get_reply = device.get(('subtree', get_filter))
    nc_get_reply_no_ns = remove_namespaces(nc_get_reply.data_ele)
    xml_rsp = nc_get_reply_no_ns.find('.//kickstart_ver_str')
    value = xml_rsp.text
    print(value)
