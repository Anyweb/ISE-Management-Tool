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

    # -- Create and delete Endpoints --
    eps = []
    eps.append(Endpoint(mac="00:01:02:03:04:06", description="description"))
    endpoint_create = manager.createEndpoints(eps)
    print(endpoint_create)
    endpoint_delete = manager.deleteEndpoints(eps)
    print(endpoint_delete)

    # -- Create and delete EndpointGroups --
    egs = []
    egs.append(EndpointGroup(name="TestGBenAbou123", description="myDescr"))
    endpointgroup_create = manager.createEndpointGroups(egs)
    print(endpointgroup_create)
    endpointgroup_delete = manager.deleteEndpointGroups(egs)
    print(endpointgroup_delete)
