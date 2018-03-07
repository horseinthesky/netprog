#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from uniq.apis.nb.client_manager import NbClientManager

client = NbClientManager(
    server="192.168.0.10",
    username="admin",
    password="Cisco123!",
    connect=True)

# NorthBound API call to get all users
user_list_result = client.user.getUsers()

# Serialize the model object to a python dictionary
users = client.serialize(user_list_result)

print(users)
