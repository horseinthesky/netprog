#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ydk.services import CRUDService
from ydk.providers import NetconfServiceProvider
from ydk.models.openconfig import openconfig_bgp as bgp

if __name__ == "__main__":
    provider = NetconfServiceProvider(
        address='10.10.10.4',
        port=22,
        username="cisco",
        password="cisco",
        protocol="ssh"
    )

    crud = CRUDService()
    bgp = bgp.Bgp()
    bgp.global_.config.as_ = 65141
    bgp.global_.config.router_id = '1.1.1.1'
    crud.create(provider, bgp)
