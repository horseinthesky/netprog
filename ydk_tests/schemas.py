from ncclient import manager
import logging
import sys

from devices import DEVICES

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    stream=sys.stdout
)

device = DEVICES['junos']

m = manager.connect(
    host=device['ip'],
    port=830,
    hostkey_verify=False,
    username='admin',
    password=device['pass'],
    device_params={'name': device['type']}
)

# for c in m.server_capabilities:
#     print(c)

schemas = ['openconfig-bgp', 'openconfig-acl', 'openconfig-inet-types']

for s in schemas:
    schema = m.get_schema(s)
    with open('{}_{}.yang'.format(device['type'], s), 'w') as f:
        f.write(schema.data)
