from requesthandler import RequestHandler

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

    def getAllEndpoints(self) -> list:
        return self.connector.getAllEndpoints()

    def createEndpoints(self, endpoints: list) -> str:
        output: str = ""
        for e in endpoints:
            output += self.connector.createEndpoint(e)
        output += f"\nProcessed {len(endpoints)} Endpoint(s)."
        return output

    def deleteEndpoints(self, endpoints: list) -> str:
        output: str = ""
        for e in endpoints:
            output += self.connector.deleteEndpoint(e)
        output += f"\nProcessed {len(endpoints)} Endpoint(s)."
        return output

    def getAllEndpointGroups(self) -> list:
        return self.connector.getAllEndpointGroups()

    def createEndpointGroups(self, endpointgroups: list) -> str:
        output: str = ""
        for eg in endpointgroups:
            output += self.connector.createEndpointGroup(eg)
        output += f"\nProcessed {len(endpointgroups)} Endpoint(s)."
        return output

    def deleteEndpointGroups(self, endpointgroups: list) -> str:
        output: str = ""
        for eg in endpointgroups:
            output += self.connector.deleteEndpointGroup(eg)
        output += f"\nProcessed {len(endpointgroups)} Endpoint(s)."
        return output
    
    def deleteEndpointGroupsWithTheirEndpoints(self, endpointgroups: list) -> str:
        output: str = ""
        endpoints: list = []
        total_endpoints: int = 0

        for eg in endpointgroups:
            endpoints = self.connector.getEndpointsOfEndpointGroup(eg)
            for e in endpoints:
                output += self.connector.deleteEndpoint(eg)
            total_endpoints += len(endpoints)
        output += f"\nProcessed {total_endpoints} Endpoint(s)."
        return output