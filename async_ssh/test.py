import asyncssh
import asyncio
import xmltodict
import json
import logging

from exceptions import RPCError
asyncssh.set_debug_level(1)

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(filename)s:%(lineno)d - %(funcName)s() - %(levelname)s - %(message)s")

hello = '''
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <capabilities>
        <capability>urn:ietf:params:netconf:base:1.0</capability>
    </capabilities>
</hello>
]]>]]>
'''
commit = '''
<rpc>
  <commit/>
</rpc>
]]>]]>
'''
close = '''
<rpc message-id="1024" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session/>
</rpc>
]]>]]>
'''
get = '''
<rpc message-id="1024" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <get>
    <filter type="subtree">
      {}
    </filter>
  </get>
</rpc>
]]>]]>
'''
edit = '''
<rpc message-id="1" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running/>
    </target>
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
      {}
    </config>
  </edit-config>
</rpc>
]]>]]>
'''
rpc = '''
<rpc message-id="1024" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  {}
</rpc>
]]>]]>
'''
power_rpc = '<get-power-usage-information/>'
commit_rpc = '<get-commit-information/>'
re_rpc = '<get-route-engine-information/>'
mem_rpc = '<get-system-memory-information/>'


class NetconfConnection:
    def __init__(self, ip):
        self.ip = ip

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, *exception):
        self.write(close)
        # self.conn.close()
        self.writer.write_eof()
        # await self.conn.wait_closed()

    async def connect(self):
        self.conn, _ = await asyncssh.create_connection(None, self.ip, known_hosts=None, username='admin', password='Juniper')
        self.writer, self.reader, _ = await self.conn.open_session(subsystem='netconf')
        self.caps = await self.read()
        self.write(hello)
        await asyncio.sleep(.1)

    async def read(self):
        data = await self.reader.readuntil(']]>]]>')
        logging.debug("read %s", data)
        return data[:-6]

    def write(self, data):
        logging.debug("write %s", data)
        self.writer.write(data)

    async def get(self, data):
        self.write(get.format(data))
        rpc_reply = await self.read()
        data = xmltodict.parse(rpc_reply)['nc:rpc-reply']
        if 'nc:rpc-error' in data:
            raise RPCError(data['nc:rpc-error']['nc:error-info']['nc:bad-element'])
        return data

    async def edit(self, data):
        self.write(edit.format(data))
        rpc_reply = await self.read()
        data = xmltodict.parse(rpc_reply)['nc:rpc-reply']
        if 'nc:rpc-error' in data:
            raise RPCError(data['nc:rpc-error']['nc:error-info']['nc:bad-element'])
        # self.write(commit)
        # data = await self.read()
        return data

    async def rpc(self, data):
        self.write(rpc.format(data))
        rpc_reply = await self.read()
        data = xmltodict.parse(rpc_reply)['nc:rpc-reply']
        if 'nc:rpc-error' in data:
            raise RPCError(data['nc:rpc-error']['nc:error-info']['nc:bad-element'])
        # self.write(commit)
        # data = await self.read()
        return data


async def get_data(device):
    async with NetconfConnection(device) as nc:
        re_reply = await nc.rpc(re_rpc)
        print(json.dumps(re_reply, indent=2))
        power_reply = await nc.rpc(power_rpc)
        print(json.dumps(power_reply, indent=2))


loop = asyncio.get_event_loop()
loop.run_until_complete(get_data('10.10.30.4'))
