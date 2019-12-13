import logging

from ydk.services import NetconfService, Datastore, CodecService
from ydk.providers import NetconfServiceProvider, CodecServiceProvider

logger = logging.getLogger('ydk')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                               "%(levelname)s - %(message)s"))
handler.setFormatter(formatter)
logger.addHandler(handler)

DEVICES = {
    'junos': {
        'ip': '10.10.30.4',
        'pass': 'Juniper'
    },
    'xr': {
        'ip': '10.10.30.5',
        'pass': 'admin'
    },
    'xe': {
        'ip': '10.10.30.6',
        'pass': 'admin'
    }
}

if __name__ == '__main__':
    device = DEVICES['xe']

    provider = NetconfServiceProvider(
        address=device['ip'],
        port=830,
        username='admin',
        password=device['pass'],
        protocol='ssh'
    )

    netconf = NetconfService()
    config = netconf.get_config(provider, Datastore.running)

    codec = CodecService()
    pr = CodecServiceProvider(type='xml')

    xml_list = codec.encode(pr, config.entities(), pretty=True)
    print('\nGOT DEVICE CONFIGURATION:\n{}'.format('\n'.join(xml_list)))
