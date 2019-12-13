from ncclient import manager
import logging
import sys
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    stream=sys.stdout
)

DEVICES = {
    'junos': {
        'ip': '10.10.30.4',
        'pass': 'Juniper',
        'type': 'junos'
    },
    'xr': {
        'ip': '10.10.30.5',
        'pass': 'admin',
        'type': 'iosxr'
    },
    'xe': {
        'ip': '10.10.30.6',
        'pass': 'admin',
        'type': 'iosxe'
    }
}

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
