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

    def getAllEndpoints(self):
        return self.connector.getAllEndpoints()

    def createEndpoints(self, endpoints: list) -> str:
        output: str = ""
        for endpoint in endpoints:
            output += self.connector.createEndpoint(endpoint)
        output += f"\nProcessed {len(endpoints)} Endpoint(s)."
        return output

    def deleteEndpoints(self, endpoints: list) -> str:
        output: str = ""
        for endpoint in endpoints:
            output += self.connector.deleteEndpoint(endpoint)
        output += f"\nProcessed {len(endpoints)} Endpoint(s)."
        return output

    def getAllEndpointGroups(self):
        return None

    def createEndpointGroups(self):
        return None

    def deleteEndpointGroups(self):
        return None