import logging

from ydk.services import NetconfService, Datastore
from ydk.providers import NetconfServiceProvider
from ydk.models.cisco_ios_xe import Cisco_IOS_XE_native as xe_native

logger = logging.getLogger('ydk')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                              "%(levelname)s - %(message)s"))
handler.setFormatter(formatter)
logger.addHandler(handler)

DEVICES = ['10.10.30.4', '10.10.30.5', '10.10.30.6']


if __name__ == '__main__':
    # provider = CodecServiceProvider(type='xml')
    # codec = CodecService()

    native = xe_native.Native()

    # print(codec.encode(provider, native))

    provider = NetconfServiceProvider(
        address='10.10.30.6',
        port=22,
        username='admin',
        password='admin',
        protocol='ssh'
    )

    netconf = NetconfService()
    config = netconf.get_config(provider, Datastore.running)
    print(config)
