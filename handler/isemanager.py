from typing import Optional

from model.endpointgroup import EndpointGroup
from handler.requesthandler import RequestHandler, FilterOperator



class ISEManagerLight:
    """
        Author:         Gabriel Ben Abou @ Anyweb
        Date:           09.07.2021
        Version:        v1.0
        Description:    This Class interacts with the Connector-Class and contains different Operations
    """
    connector: RequestHandler

    def __init__(self):
        """Initilizes an instance of RequestHandler
        """
        self.connector = RequestHandler()

    def getAllEndpoints(self, filter: Optional[str], filterOperator: Optional[FilterOperator]) -> list:
        """Retrieves all Endpoints and returns them

        Args:
            filter (Optional[str]): Filter for MAC-Adress
            filterOperator (Optional[FilterOperator]): An ENUM of FilterOperator

        Returns:
            list: All Endpoints
        """
        eps = self.connector.getAllEndpoints(filter, filterOperator)
        for e in eps:
            print(repr(e))
        return eps

    def getAllEndpointGroups(self, filter: Optional[str], filterOperator: Optional[FilterOperator]) -> list:
        """Retrieves all Endpoint groups and returns

        Args:
            filter (Optional[str]): Filter for Name of a Group
            filterOperator (Optional[FilterOperator]): An ENUM of FilterOperator

        Returns:
            list: All Endpoint Groups in JSON format
        """
        egs = self.connector.getAllEndpointGroups(filter, filterOperator)
        return egs

    def getEndpointsOfEndpointGroup(self, endpointgroup: EndpointGroup) -> list:
        """Retrieve all Endpoints of the specified Endpoint Group

        Args:
            endpointgroup (EndpointGroup): An EndpointGroup object

        Returns:
            list: All Endpoints of the specified Endpoint Group
        """
        eps = self.connector.getEndpointsOfEndpointGroup(endpointgroup)
        return eps

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
        endpoints_length:int = len(endpoints) 
        current_run: int = 0

        for e in endpoints:
            output += self.connector.deleteEndpoint(e)
            current_run += 1
            print(f"Processed {current_run}/{endpoints_length} Endpoint(s).", end='\r')
        output += f"\nProcessed {endpoints_length} Endpoint(s)."
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
        output += f"\nProcessed {len(endpointgroups)} Endpoint Group(s)."
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
