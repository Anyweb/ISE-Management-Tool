from typing import Optional

from endpointgroup import EndpointGroup
from requesthandler import FilterOperator, RequestHandler

"""
Author:         Gabriel Ben Abou @ Anyweb
Date:           09.07.2021
Version:        v1.0
Description:    This Class interacts with the Connector-Class and contains different Operations
"""

class ISEManager:
    connector: RequestHandler

    def __init__(self):
        """Initilizes an instance of RequestHandler
        """
        self.connector = RequestHandler()

    def getAllEndpoints(self, filter: Optional[str], filterOperator: Optional[FilterOperator]) -> str:
        """Retrieves all Endpoints and returns them as a result String

        Args:
            filter (Optional[str]): Filter for MAC-Adress
            filterOperator (Optional[FilterOperator]): An ENUM of FilterOperator

        Returns:
            str: All Endpoints in JSON format
        """
        output: str = "\n-- Get All Endpoint(s): --"
        for e in self.connector.getAllEndpoints(filter, filterOperator):
            output += "\n" + repr(e)
        return output

    def getAllEndpointGroups(self, filter: Optional[str], filterOperator: Optional[FilterOperator]) -> str:
        """Retrieves all Endpoint groups and returns them as String

        Args:
            filter (Optional[str]): Filter for Name of a Group
            filterOperator (Optional[FilterOperator]): An ENUM of FilterOperator

        Returns:
            str: All Endpoint Groups in JSON format
        """
        output: str = "\n-- Get All Endpoint Group(s): --"
        for e in self.connector.getAllEndpointGroups(filter, filterOperator):
            output += "\n" + repr(e)
        return output

    def getListOfAllEndpointGroups(self, filter: Optional[str], filterOperator: Optional[FilterOperator]) -> list:
        """Retrieve all Endpoint Groups and return them as List of EndpointGroup objects

        Args:
            filter (Optional[str]): Filter for Name of a Group  
            filterOperator (Optional[FilterOperator]): An ENUM of FilterOperator

        Returns:
            list: All Endpoint Group objects
        """
        return self.connector.getAllEndpointGroups(filter, filterOperator)
            

    def getEndpointsOfEndpointGroup(self, endpointgroup: EndpointGroup) -> str:
        """Retrieve all Endpoints of the specified Endpoint Group

        Args:
            endpointgroup (EndpointGroup): An EndpointGroup object

        Returns:
            str: All Endpoints of the specified Endpoint Group
        """
        output: str = "-- Getting Endpoint(s) of an Endpoint Group: --"
        for e in self.connector.getEndpointsOfEndpointGroup(endpointgroup):
            output += "\n" + repr(e)
        return output

    def createEndpoints(self, endpoints: list) -> str:
        """Create new endpoints

        Args:
            endpoints (list): A list of endpoints

        Returns:
            str: Response and failures
        """
        output: str = "-- Creating Endpoint(s): --"
        for e in endpoints:
            output += self.connector.createEndpoint(e)
        output += f"\nProcessed {len(endpoints)} Endpoint(s)."
        return output

    def deleteEndpoints(self, endpoints: list) -> str:
        """Delete Endpoints

        Args:
            endpoints (list): A list of endpoints

        Returns:
            str: Response and failures
        """
        output: str = "-- Deleting Endpoint(s): --"
        for e in endpoints:
            output += self.connector.deleteEndpoint(e)
        output += f"\nProcessed {len(endpoints)} Endpoint(s)."
        return output

    def createEndpointGroups(self, endpointgroups: list) -> str:
        """Create new endpoint groups

        Args:
            endpointgroups (list): A list of endpoint groups

        Returns:
            str: Response and failures
        """
        output: str = "-- Creating Endpoint Group(s): --"
        for eg in endpointgroups:
            output += self.connector.createEndpointGroup(eg)
        output += f"\nProcessed {len(endpointgroups)} Endpoint Group(s)."
        return output

    def deleteEndpointGroups(self, endpointgroups: list) -> str:
        """Delete endpoint groups

        Args:
            endpointgroups (list): A list of endpoint groups

        Returns:
            str: Response and failures
        """
        output: str = "-- Deleting Endpoint Group(s): --"
        for eg in endpointgroups:
            output += self.connector.deleteEndpointGroup(eg)
        output += f"\nProcessed {len(endpointgroups)} Endpoint(s)."
        return output
    
    def deleteEndpointGroupsWithTheirEndpoints(self, endpointgroups: list) -> str:
        """Delete Endpoint Groups and delete all endpoints that match that group

        Args:
            endpointgroups (list): A list of endpoint groups

        Returns:
            str: Response and failures
        """
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

    def addEndpointsToGroup(self, endpoints: list, endpointGroup: EndpointGroup) -> str:
        """Add endpoints to an endpoint group

        Args:
            endpoints (list): A list of endpoints
            endpointGroup (EndpointGroup): An EndpointGroup object

        Returns:
            str: Response and failures
        """
        output: str = "-- Add Endpoint(s) to Group: --"
        for e in endpoints:
            output += self.connector.addEndpointToGroup(e, endpointGroup)
        output += f"\nProcessed {len(endpoints)} Endpoint(s)."
        return output
