import logging

from ydk.services import CodecService, CRUDService
from ydk.providers import CodecServiceProvider, NetconfServiceProvider
from ydk.models.openconfig import openconfig_bgp as oc_bgp
from ydk.models.openconfig import openconfig_network_instance as oc_ni
from ydk.models.openconfig import openconfig_policy_types as oc_policy
from ydk.models.openconfig import openconfig_bgp_types as oc_bgp_types
from ydk.filters import YFilter

from devices import DEVICES

logger = logging.getLogger('ydk')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                               "%(levelname)s - %(message)s"))
handler.setFormatter(formatter)
logger.addHandler(handler)


def config_bgp(bgp):
    """Add config data to bgp object."""
    # global configuration
    bgp.global_.config.as_ = 5
    afi_safi = bgp.global_.afi_safis.AfiSafi()
    afi_safi.afi_safi_name = oc_bgp_types.IPV6UNICAST()
    afi_safi.config.afi_safi_name = oc_bgp_types.IPV6UNICAST()
    afi_safi.config.enabled = True
    bgp.global_.afi_safis.afi_safi.append(afi_safi)

    # configure IBGP peer group
    peer_group = bgp.peer_groups.PeerGroup()
    peer_group.peer_group_name = "EBGP"
    peer_group.config.peer_group_name = "EBGP"
    peer_group.config.peer_as = 6
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
    neighbor.neighbor_address = '10.10.30.6'
    neighbor.config.neighbor_address = '10.10.30.6'
    neighbor.config.peer_group = "EBGP"
    bgp.neighbors.neighbor.append(neighbor)


if __name__ == '__main__':
    nis = oc_ni.NetworkInstances()
    ni = oc_ni.NetworkInstances.NetworkInstance()    # list element has 1 key
    ni.name = 'default'    # must define network instance key
    nis.network_instance.append(ni)   # must add network instance to the list

    pr = oc_ni.NetworkInstances.NetworkInstance.Protocols.Protocol()  # list element has 2 keys
    pr.name = 'BGP-5'  # must define protocol key
    pr.identifier = oc_policy.BGP()  # must define protocol key

    ni.protocols.protocol.append(pr)  # must add protocol to the list

    # Also need to define protocol.config attributes
    pr.config.name = 'BGP-5'
    pr.config.identifier = oc_policy.BGP()
    pr.config.enabled = True

    bgp = pr.bgp   # bgp is attribute of protocol and has already been instantiated above
    config_bgp(bgp)

    # codec = CodecService()
    # pr = CodecServiceProvider(type='xml')
    # print(codec.encode(pr, nis))
    device = DEVICES['junos']

    provider = NetconfServiceProvider(
        address=device['ip'],
        port=830,
        username='admin',
        password=device['pass'],
        protocol='ssh'
    )
    crud = CRUDService()
    crud.create(provider, nis)
