import asyncssh
import asyncio
import xmltodict
import json
import logging

from exceptions import RPCError
asyncssh.set_debug_level(2)

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(filename)s:%(lineno)d - %(funcName)s() - %(levelname)s - %(message)s")

hello = '''
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <capabilities>
        <capability>urn:ietf:params:netconf:base:1.0</capability>
    </capabilities>
</hello>
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
cpu_rpc = '''<devm xmlns="http://www.huawei.com/netconf/vrp/huawei-devm">
        <cpuInfos>
          <cpuInfo>
            <systemCpuUsage></systemCpuUsage>
          </cpuInfo>
        </cpuInfos>
      </devm>'''
intf_rpc = '''<ethernet xmlns="http://www.huawei.com/netconf/vrp/huawei-ethernet">
        <ethernetIfs>
           <ethernetIf>
             <ifName>25GE1/0/11</ifName>
             <l2Enable>enable</l2Enable>
             <l2Attribute>
               <linkType>trunk</linkType>
               <pvid>106</pvid>
               <trunkVlans>4,5,6,104,106</trunkVlans>
               <taggedPacketDiscard>false</taggedPacketDiscard>
               <portBridgEnable>false</portBridgEnable>
             </l2Attribute>
           </ethernetIf>
        </ethernetIfs>
      </ethernet>'''


class NetconfConnection:
    def __init__(self, ip):
        self.ip = ip

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, *exception):
        self.write(close)
        await self.conn.wait_closed()

    async def connect(self):
        self.conn, _ = await asyncssh.create_connection(None, self.ip, known_hosts=None)
        self.writer, self.reader, _ = await self.conn.open_session(subsystem='netconf')
        self.caps = await self.read()
        self.write(hello)

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
        data = xmltodict.parse(rpc_reply)['rpc-reply']
        if 'rpc-error' in data:
            raise RPCError(data['rpc-error']['error-message']['#text'])
        return data

    async def edit(self, data):
        self.write(edit.format(data))
        rpc_reply = await self.read()
        data = xmltodict.parse(rpc_reply)['rpc-reply']
        if 'rpc-error' in data:
            raise RPCError(data['rpc-error']['error-message']['#text'])
        return data


async def get_data(device):
    async with NetconfConnection(device) as nc:
        intf_rpc_reply = await nc.edit(intf_rpc)
        print(json.dumps(intf_rpc_reply, indent=2))
        cpu_rpc_reply = await nc.get(cpu_rpc)
        print(json.dumps(cpu_rpc_reply, indent=2))


loop = asyncio.get_event_loop()
loop.run_until_complete(get_data('hostname'))
