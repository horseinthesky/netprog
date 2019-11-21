from ncclient import manager
import logging
import sys
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    stream=sys.stdout
)

m = manager.connect(
    host='10.10.30.6',
    port=22,
    username='admin',
    password='admin',
    device_params={'name': 'csr'}
)

# for c in m.server_capabilities:
#     print(c)

schema = m.get_schema('openconfig-acl')
with open('openconfig-acl.yang', 'w') as f:
    f.write(schema.data)

inet_types = m.get_schema('openconfig-inet-types')
with open('openconfig-inet-types.yang', 'w') as f:
    f.write(inet_types.data)
