from model.endpoint import Endpoint
from model.endpointgroup import EndpointGroup
from handler.isemanager import ISEManagerLight
from handler.requesthandler import FilterOperator

"""
Author:         Gabriel Ben Abou @ Anyweb
Date:           09.07.2021
Version:        v1.0
Description:    
"""
   
if __name__ == '__main__':
    manager = ISEManagerLight() 

    egs = []
    eg = EndpointGroup(name="TestGBenAbou123", description="myDescr")
    egs.append(eg)
    print(manager.createEndpointGroups(egs))

    eps = []
    eps.append(Endpoint(mac="00:01:02:03:04:06", description="description"))
    eps.append(Endpoint(mac="00:01:02:03:04:16", description="description"))
    print(manager.createEndpoints(eps))

    print(manager.addEndpointsToGroup(eps, eg))
    print(manager.getEndpointsOfEndpointGroup(eg))

    print(manager.deleteEndpointGroupsWithTheirEndpoints(egs))
    print(manager.getEndpointsOfEndpointGroup(eg))
    
    # Check filtering
    print(manager.getAllEndpointGroups(filter="test", filterOperator=FilterOperator.NOT_CONTAINS))
    print(manager.getAllEndpoints(filter="00:01:02", filterOperator=FilterOperator.CONTAINS))

    print(manager.createEndpoints(eps))
    print(manager.deleteEndpoints(eps))
