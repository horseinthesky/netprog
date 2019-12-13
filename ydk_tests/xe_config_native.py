from ydk.services import CRUDService, CodecService
from ydk.providers import NetconfServiceProvider, CodecServiceProvider
from ydk.models.cisco_ios_xe.Cisco_IOS_XE_native import Native

import yaml
import logging

from recursive import instantiate

logger = logging.getLogger('ydk')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                               "%(levelname)s - %(message)s"))
handler.setFormatter(formatter)
logger.addHandler(handler)

if __name__ == '__main__':
    with open('xe_config_native.yml') as f:
        config = yaml.load(f)['config']

    for model_name, model_data in config.items():
        for k, v in model_data.items():
            binding = globals().get(model_name.capitalize())()
            instantiate(binding, k, v)

    # codec = CodecService()
    # provider = CodecServiceProvider(type='xml')
    # print(codec.encode(provider, native))
    provider = NetconfServiceProvider(
        address='10.10.30.6',
        port=830,
        username='admin',
        password='admin',
        protocol='ssh'
    )
    crud = CRUDService()
    crud.create(provider, binding)
