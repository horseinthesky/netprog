import logging

from ydk.services import CodecService, CRUDService
from ydk.providers import CodecServiceProvider, NetconfServiceProvider
from ydk.models.openconfig import openconfig_acl as oc_acl

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


def config_acl(acl):
    """Add config data to acl object."""
    # acl-set configuration
    acl_set = acl.AclSets.AclSet()
    acl_set.name = "ACL3"
    acl_set.type = oc_acl.ACLIPV4()
    acl_set.config.name = "ACL3"
    acl_set.config.type = oc_acl.ACLIPV4()
    acl_set.acl_entries = acl_set.AclEntries()
    # acl-entry with sequence number 20
    acl_entry = acl_set.acl_entries.AclEntry()
    acl_entry.sequence_id = 20
    # acl_entry.config.sequence_id = 20
    acl_entry.actions.config.forwarding_action = oc_acl.REJECT()
    acl_entry.ipv4.config.source_address = "173.31.1.0/24"
    acl_entry.ipv4.config.destination_address = "172.16.0.0/16"
    acl_set.acl_entries.acl_entry.append(acl_entry)
    # acl-entry with sequence number 30
    acl_entry = acl_set.acl_entries.AclEntry()
    acl_entry.sequence_id = 30
    acl_entry.config.sequence_id = 30
    acl_entry.actions.config.forwarding_action = oc_acl.REJECT()
    acl_entry.ipv4.config.source_address = "172.31.2.0/24"
    acl_entry.ipv4.config.destination_address = "172.16.0.0/16"
    acl_entry.ipv4.config.dscp = 46
    acl_set.acl_entries.acl_entry.append(acl_entry)
    # acl-entry with sequence number 40
    acl_entry = acl_set.acl_entries.AclEntry()
    acl_entry.sequence_id = 40
    acl_entry.config.sequence_id = 40
    acl_entry.actions.config.forwarding_action = oc_acl.REJECT()
    acl_entry.ipv4.config.source_address = "172.31.3.0/24"
    acl_entry.ipv4.config.destination_address = "172.16.0.0/16"
    acl_set.acl_entries.acl_entry.append(acl_entry)
    # acl-entry with sequence number 50
    acl_entry = acl_set.acl_entries.AclEntry()
    acl_entry.sequence_id = 50
    acl_entry.config.sequence_id = 50
    acl_entry.actions.config.forwarding_action = oc_acl.ACCEPT()
    acl_set.acl_entries.acl_entry.append(acl_entry)
    acl.acl_sets.acl_set.append(acl_set)


if __name__ == '__main__':
    # provider = CodecServiceProvider(type='xml')
    # codec = CodecService()

    acl = oc_acl.Acl()
    config_acl(acl)
    # print(codec.encode(provider, acl))

    device = DEVICES['xr']

    provider = NetconfServiceProvider(
        address=device['ip'],
        port=830,
        username='admin',
        password=device['pass'],
        protocol='ssh'
    )

    crud = CRUDService()
    crud.create(provider, acl)
