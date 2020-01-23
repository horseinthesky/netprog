#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import aiohttp
import asyncssh
import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(filename)s:%(lineno)d - %(funcName)s() - %(levelname)s - %(message)s")

devices = ['cloud-sas2-92fvrr1.cloud.yandex.net', 'cloud-vla1-4fvrr1.cloud.yandex.net']

hello = '''
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <capabilities>
        <capability>urn:ietf:params:netconf:base:1.0</capability>
    </capabilities>
</hello>
]]>]]>
'''
msg = '''
<rpc message-id="1024" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    {}
</rpc>
]]>]]>
'''
rpc = '<get-power-usage-information/>'

NB_URL = 'http://netbox.cloud.yandex.net/api'


async def fetch_fvrrs(session, url):
    async with session.get(url + '/virtualization/virtual-machines/') as response:
        vms = (await response.json())['results']
    async with session.get(url + '/dcim/devices/?role=server') as response:
        servers = (await response.json())['results']

    fvrrs = {}
    for vm in vms:
        if 'reflector' in vm['role']['slug']:
            if vm['tenant']['slug'] == 'production':
                hostname = vm['name']
                vendor = vm['custom_fields']['type'].split()[0].lower()
                for server in servers:
                    if vm['custom_fields']['host_machine'] == server['name']:
                        location = server['site']['slug']

                if vm['role']['slug'] == 'fv-route-reflector':
                    fvrrs[hostname] = {
                        'ip': vm['primary_ip6']['address'].split('/')[0],
                        'vendor': vendor,
                        'localtion': location
                    }
    return fvrrs


class netconf:
    async def connect(self, ip):
        self.conn, _ = await asyncssh.create_connection(None, ip, known_hosts=None)
        self.writer, self.reader, _ = await self.conn.open_session(subsystem='netconf')
        self.caps = await self.read()

    async def read(self):
        data = await self.reader.readuntil(']]>]]>')
        logging.debug("read %s", data)
        return data

    def write(self, data):
        self.writer.write(data)
        logging.debug("write %s", data)

    async def cmd(self, data):
        self.write(data)
        data = await self.read()
        return data


async def run_client(device):
    n = netconf()
    await n.connect(device)
    n.write(hello)

    while True:
        await n.cmd(msg.format(rpc))
        await asyncio.sleep(10)


async def main():
    running = {}

    while True:

        async with aiohttp.ClientSession() as session:
            fvrrs = await fetch_fvrrs(session, NB_URL)

        for host in fvrrs:
            if host not in running:
                logging.debug("start run_client() on host %s", host)
                task = run_client(fvrrs[host]['ip'])
                future = asyncio.ensure_future(task)
                running[host] = future

        for host in running:
            if host not in fvrrs:
                logging.debug("stop run_client() on host %s", host)
                running[host].cancel()
                del running[host]

        await asyncio.sleep(30)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
