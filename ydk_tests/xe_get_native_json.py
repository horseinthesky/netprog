import logging

from ydk.services import NetconfService, Datastore
from ydk.providers import NetconfServiceProvider
from ydk.entity_utils import JsonSubtreeCodec

from devices import DEVICES

logger = logging.getLogger('ydk')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                               "%(levelname)s - %(message)s"))
handler.setFormatter(formatter)
logger.addHandler(handler)

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

    jcodec = JsonSubtreeCodec()

    payload = jcodec.encode(config.entities()[0], provider.get_session().get_root_schema(), True)
    print(payload)
