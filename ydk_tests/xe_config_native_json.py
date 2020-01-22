from ydk.services import CRUDService, CodecService
from ydk.providers import NetconfServiceProvider, CodecServiceProvider
from ydk.models.cisco_ios_xe.Cisco_IOS_XE_native import Native

import yaml
import json
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
    with open('xe_config_native_json.yml', 'r') as yaml_config:
        config_dict = yaml.safe_load(yaml_config)
        json_str = json.dumps(config_dict, indent=2)
        # print(json_str)

    codec = CodecService()
    codec_provider = CodecServiceProvider(type='json')
    binding = codec.decode(codec_provider, json_str)
    # print(codec.encode(codec_provider, binding))

    provider = NetconfServiceProvider(
        address='10.10.30.6',
        port=830,
        username='admin',
        password='admin',
        protocol='ssh'
    )
    crud = CRUDService()
    crud.create(provider, binding)
