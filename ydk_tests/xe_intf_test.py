from ydk.services import CRUDService, CodecService
from ydk.providers import NetconfServiceProvider, CodecServiceProvider
from ydk.types import Empty
from ydk.models.cisco_ios_xe import Cisco_IOS_XE_native as xe_native
from ydk.filters import YFilter
import yaml
import logging

logger = logging.getLogger('ydk')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                               "%(levelname)s - %(message)s"))
handler.setFormatter(formatter)
logger.addHandler(handler)

if __name__ == '__main__':
    native = xe_native.Native()
    with open('interfaces.yml') as f:
        interfaces = yaml.load(f)

    for kind, intf_data in interfaces['interface'].items():
        l1 = getattr(native.interface, kind.lower())
        for intf in intf_data:
            yintf_instance = getattr(native.interface, kind)
            yintf = yintf_instance()
            yintf.name = intf['name']
            yintf.description = intf['description']
            if 'secondary' in intf['ip']['address']:
                for addr in intf['ip']['address']['secondary']:
                    sec = yintf.ip.address.Secondary()
                    sec.address = addr['address']
                    sec.mask = addr['mask']
                    sec.secondary = Empty()
                    yintf.ip.address.secondary.append(sec)

            yintf.ip.address.primary.address = intf['ip']['address']['primary']['address']
            yintf.ip.address.primary.mask = intf['ip']['address']['primary']['mask']

            yintf.yfilter = YFilter.replace
            l1.append(yintf)

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
    crud.create(provider, native)
