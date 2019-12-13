import logging

from ydk.services import CRUDService
from ydk.providers import NetconfServiceProvider
from ydk.models.cisco_ios_xe import Cisco_IOS_XE_native as xe_native
from ydk.filters import YFilter

logger = logging.getLogger('ydk')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                               "%(levelname)s - %(message)s"))
handler.setFormatter(formatter)
logger.addHandler(handler)


def config_interface(native):
    gigabitethernet = native.interface.GigabitEthernet()
    gigabitethernet.yfilter = YFilter.replace

    gigabitethernet.name = "2"
    gigabitethernet.description = "Configured via ydk"
    gigabitethernet.mtu = 9192
    gigabitethernet.load_interval = 30

    gigabitethernet.ip.address.primary.address = "172.16.1.0"
    gigabitethernet.ip.address.primary.mask = "255.255.255.254"

    prefix_list = gigabitethernet.ipv6.address.PrefixList()
    prefix_list.prefix = '2001:db8::1:0/127'
    gigabitethernet.ipv6.address.prefix_list.append(prefix_list)

    native.interface.gigabitethernet.append(gigabitethernet)


if __name__ == '__main__':
    native = xe_native.Native()
    config_interface(native)

    provider = NetconfServiceProvider(
        address='10.10.30.6',
        port=830,
        username='admin',
        password='admin',
        protocol='ssh'
    )
    crud = CRUDService()
    crud.create(provider, native)
