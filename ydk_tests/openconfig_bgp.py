import logging

from ydk.services import CodecService, CRUDService
from ydk.providers import CodecServiceProvider, NetconfServiceProvider
from ydk.models.openconfig import openconfig_bgp as oc_bgp
from ydk.models.openconfig import openconfig_bgp_types as oc_bgp_types
from ydk.filters import YFilter

logger = logging.getLogger('ydk')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                               "%(levelname)s - %(message)s"))
handler.setFormatter(formatter)
logger.addHandler(handler)

DEVICES = ['10.10.30.4', '10.10.30.5', '10.10.30.6']


def config_bgp(bgp):
    """Add config data to bgp object."""
    # global configuration
    bgp.global_.config.as_ = 65001
    afi_safi = bgp.global_.afi_safis.AfiSafi()
    afi_safi.afi_safi_name = oc_bgp_types.IPV6UNICAST()
    afi_safi.config.afi_safi_name = oc_bgp_types.IPV6UNICAST()
    afi_safi.config.enabled = True
    bgp.global_.afi_safis.afi_safi.append(afi_safi)

    # configure IBGP peer group
    peer_group = bgp.peer_groups.PeerGroup()
    peer_group.peer_group_name = "EBGP"
    peer_group.config.peer_group_name = "EBGP"
    peer_group.config.peer_as = 65002
    peer_group.transport.config.local_address = "Loopback0"
    afi_safi = peer_group.afi_safis.AfiSafi()
    afi_safi.afi_safi_name = oc_bgp_types.IPV6UNICAST()
    afi_safi.config.afi_safi_name = oc_bgp_types.IPV6UNICAST()
    afi_safi.config.enabled = True
    # afi_safi.apply_policy.config.import_policy.append("POLICY3")
    # afi_safi.apply_policy.config.export_policy.append("POLICY1")
    peer_group.afi_safis.afi_safi.append(afi_safi)
    bgp.peer_groups.peer_group.append(peer_group)

    # configure IBGP neighbor
    neighbor = bgp.neighbors.Neighbor()
    neighbor.neighbor_address = '2001:db8:e:1::1'
    neighbor.config.neighbor_address = '2001:db8:e:1::1'
    neighbor.config.peer_group = "EBGP"
    bgp.neighbors.neighbor.append(neighbor)


if __name__ == '__main__':
    # provider = CodecServiceProvider(type='xml')
    # codec = CodecService()

    bgp = oc_bgp.Bgp()
    bgp.yfilter = YFilter.replace
    config_bgp(bgp)

    # print(codec.encode(provider, native))

    provider = NetconfServiceProvider(
        address='10.10.30.5',
        port=22,
        username='admin',
        password='admin',
        protocol='ssh'
    )
    crud = CRUDService()
    crud.create(provider, bgp)
