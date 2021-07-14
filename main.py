from isemanager import ISEManager
from endpoint import Endpoint
from endpointgroup import EndpointGroup

"""
Author:         Gabriel Ben Abou @ Anyweb
Date:           09.07.2021
Version:        v1.0
Description:    
"""

if __name__ == '__main__':
    manager = ISEManager() 
    #endpoints = manager.getAllEndpoints()
    #print(f"Total Endpoints selected: {len(endpoints)}")

    endpoints = []
    endpoints.append(Endpoint(mac="00:01:02:03:04:06", description="description"))
    endpoint_create = manager.createEndpoints(endpoints)
    print(endpoint_create)
    endpoint_delete = manager.deleteEndpoints(endpoints)
    print(endpoint_delete)
    #print(f"Total Endpointgroups selected: {len(endpointgroups)}")
