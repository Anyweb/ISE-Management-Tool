from endpointgroup import EndpointGroup
from requesthandler import RequestHandler, FilterOperator
from typing import Optional

"""
Author:         Gabriel Ben Abou @ Anyweb
Date:           09.07.2021
Version:        v1.0
Description:    XXXXXXXXXXXXXX
"""

class ISEManager:
    connector: RequestHandler

    def __init__(self):
        self.connector = RequestHandler()

    def getAllEndpoints(self, filter: Optional[str], filterOperator: Optional[FilterOperator]) -> str:
        output: str = "\n-- Get All Endpoint(s): --"
        for e in self.connector.getAllEndpoints(filter, filterOperator):
            output += "\n" + repr(e)
        return output

    def getAllEndpointGroups(self, filter: Optional[str], filterOperator: Optional[FilterOperator]) -> str:
        output: str = "\n-- Get All Endpoint Group(s): --"
        for e in self.connector.getAllEndpointGroups(filter, filterOperator):
            output += "\n" + repr(e)
        return output

    def getListOfAllEndpointGroups(self, filter: Optional[str], filterOperator: Optional[FilterOperator]) -> list:
        return self.connector.getAllEndpointGroups(filter, filterOperator)
            

    def getEndpointsOfEndpointGroup(self, endpointgroup: EndpointGroup) -> str:
        output: str = "-- Getting Endpoint(s) of an Endpoint Group: --"
        for e in self.connector.getEndpointsOfEndpointGroup(endpointgroup):
            output += "\n" + repr(e)
        return output

    def createEndpoints(self, endpoints: list) -> str:
        output: str = "-- Creating Endpoint(s): --"
        for e in endpoints:
            output += self.connector.createEndpoint(e)
        output += f"\nProcessed {len(endpoints)} Endpoint(s)."
        return output

    def deleteEndpoints(self, endpoints: list) -> str:
        output: str = "-- Deleting Endpoint(s): --"
        for e in endpoints:
            output += self.connector.deleteEndpoint(e)
        output += f"\nProcessed {len(endpoints)} Endpoint(s)."
        return output

    def createEndpointGroups(self, endpointgroups: list) -> str:
        output: str = "-- Creating Endpoint Group(s): --"
        for eg in endpointgroups:
            output += self.connector.createEndpointGroup(eg)
        output += f"\nProcessed {len(endpointgroups)} Endpoint Group(s)."
        return output

    def deleteEndpointGroups(self, endpointgroups: list) -> str:
        output: str = "-- Deleting Endpoint Group(s): --"
        for eg in endpointgroups:
            output += self.connector.deleteEndpointGroup(eg)
        output += f"\nProcessed {len(endpointgroups)} Endpoint(s)."
        return output
    
    def deleteEndpointGroupsWithTheirEndpoints(self, endpointgroups: list) -> str:
        output: str = "-- Remove Endpoint Group(s) with Endpoint(s): --"
        endpoints: list = []
        total_endpoints: int = 0

        for eg in endpointgroups:
            endpoints = self.connector.getEndpointsOfEndpointGroup(eg)
            for e in endpoints:
                output += self.connector.deleteEndpoint(e)
                total_endpoints += len(endpoints)
            output += self.connector.deleteEndpointGroup(eg)
        output += f"\nProcessed {len(endpointgroups)} Endpoint Group(s) with a total of {total_endpoints} Endpoint(s)."
        return output

    def addEndpointsToGroup(self, endpoints: list, endpointGroup: EndpointGroup):
        output: str = "-- Add Endpoint(s) to Group: --"
        for e in endpoints:
            output += self.connector.addEndpointToGroup(e, endpointGroup)
        output += f"\nProcessed {len(endpoints)} Endpoint(s)."
        return output