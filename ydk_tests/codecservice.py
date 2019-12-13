from ydk.services import CodecService
from ydk.providers import CodecServiceProvider
from ydk.models.openconfig import openconfig_acl as oc_acl


def config_acl(acl):
    """Add config data to acl object."""
    # acl-set configuration
    acl_set = acl.acl_sets.AclSet()
    acl_set.name = "ACL1"
    acl_set.type = oc_acl.ACLIPV4()
    # acl_set.config.name = "ACL1"
    # acl_set.config.type = oc_acl.ACLIPV4()
    acl_set.acl_entries = acl_set.AclEntries()

    # acl-entry with sequence number 10
    acl_entry = acl_set.acl_entries.AclEntry()
    acl_entry.sequence_id = 10
    # acl_entry.config.sequence_id = 10
    acl_set.acl_entries.acl_entry.append(acl_entry)

    # acl-entry with sequence number 20
    acl_entry = acl_set.acl_entries.AclEntry()
    acl_entry.sequence_id = 20
    # acl_entry.config.sequence_id = 20
    acl_entry.ipv4.config.source_address = "172.31.255.1/32"
    acl_entry.actions.config.forwarding_action = oc_acl.ACCEPT()
    acl_set.acl_entries.acl_entry.append(acl_entry)

    # acl-entry with sequence number 30
    acl_entry = acl_set.acl_entries.AclEntry()
    acl_entry.sequence_id = 30
    # acl_entry.config.sequence_id = 30
    acl_entry.actions.config.forwarding_action = oc_acl.REJECT()
    acl_set.acl_entries.acl_entry.append(acl_entry)
    acl.acl_sets.acl_set.append(acl_set)


if __name__ == '__main__':
    provider = CodecServiceProvider(type='xml')
    codec = CodecService()

    acl = oc_acl.Acl()
    config_acl(acl)
    print(codec.encode(provider, acl))
