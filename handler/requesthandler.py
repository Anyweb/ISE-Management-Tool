import json
import os
from enum import Enum
from typing import Optional
from urllib.parse import urlparse

import requests
import urllib3
from dotenv import load_dotenv

from model.endpoint import Endpoint
from model.endpointgroup import EndpointGroup

class FilterOperator(Enum):
    EQUALS = "EQ"
    NOT_EQUALS = "NEQ"
    STARTS_WITH = "STARTSW"
    NOT_STARTS_WITH = "NSTARTSW"
    ENDS_WITH = "ENDSW"
    NOT_ENDS_WITH = "NENDSW"
    CONTAINS = "CONTAINS"
    NOT_CONTAINS = "NCONTAINS"


class RequestHandler:
    """
        Author:         Gabriel Ben Abou @ Anyweb
        Date:           09.07.2021
        Version:        v1.0
        Description:    Handles to API-Calls and Operations to the Cisco ISE-API
                Uses and .env-File to store username, password, baseurl of the Cisco ISE
    """
    ise_username: str
    ise_password: str
    ise_url: str

    def __init__(self):
        """Retrieves the environment variables from the .env-File.
            Valid Variables are: username, password, baseurl
        """
        urllib3.disable_warnings()
        load_dotenv()
        self.ise_username = os.getenv('username')
        self.ise_password = os.getenv('password')
        self.ise_url = os.getenv('baseurl')

    def getAllEndpoints(self, filter: Optional[str], filterOperator: Optional[FilterOperator]) -> list:
        """Retrieve all Endpoints that match the filter with the given filter operator
        Args:
            filter (Optional[str]): A filter for the "mac" attribute of an Endpoint.
            filterOperator (Optional[FilterOperator]): An ENUM of FilterOperator.

        Returns:
            list: A list of matching Endpoints
        """
        endpoints = [] 
        page = 1
        while page != -1:   # While not reached last page get items of next page
            jsondata = json.loads(self.__getEndpointsFiltered(page, filter, filterOperator).text)
            page = self.__getNextPageNumber(jsondata)
            for endpoint in jsondata["SearchResult"]["resources"]:
                endpoints.append(Endpoint(id=endpoint["id"],name=endpoint["name"]))
        return endpoints

    def getAllEndpointGroups(self, filter: Optional[str], filterOperator: Optional[FilterOperator]) -> list:
        """Retrieve all Endpoint Groups that match the filter with the given filter operator

        Args:
            filter (Optional[str]): A filter for the "name" attribute of an Endpoint.
            filterOperator (Optional[FilterOperator]): An ENUM of FilterOperator

        Returns:
            list: Endpoints Groups matching the filter 
        """
        endpointgroups = [] 
        page = 1
        while page != -1: 
            jsondata = json.loads(self.__getEndpointGroupsFiltered(page, filter, filterOperator).text)
            page = self.__getNextPageNumber(jsondata)
            for endpointgroup in jsondata["SearchResult"]["resources"]:
                endpointgroups.append(EndpointGroup(id=endpointgroup["id"],
                                                    name=endpointgroup["name"],
                                                    description=endpointgroup["description"]))
        return endpointgroups

    def getEndpointsOfEndpointGroup(self, endpointGroup: EndpointGroup) -> list:
        """Retrieve all Endpoints that are part of a Endpoint Group. A lookup of the ID of an Endpoint 
           Group object will done, if not set.  

        Args:
            endpointGroup (EndpointGroup): An EndpointGroup object

        Returns:
            list: List of Endpoints matching the filter
        """
        endpoints = []
        page = 1
        if endpointGroup.id == "":
            self.__populateEndpointGroupIDbyName(endpointGroup)
        groupID = endpointGroup.id

        while page != -1: 
            jsondata = json.loads(self.__getEndpointMatchingGroupIDPaginated(page, groupID).text)
            page = self.__getNextPageNumber(jsondata)
            for endpoint in jsondata["SearchResult"]["resources"]:
                endpoints.append(Endpoint(id=endpoint["id"],name=endpoint["name"]))
        return endpoints

    def createEndpoint(self, endpoint: Endpoint) -> str:
        """Create a new endpoint.

        Args:
            endpoint (Endpoint): An Endpoint object

        Returns:
            str: Failed Endpoints
        """
        output: str = ""
        resource = f"{self.ise_url}/endpoint"
        headers = {
                    'Accept': 'application/json', 
                    'Content-Type': 'application/json'
                }
        payload = repr(endpoint)
        response = requests.post(resource, auth=(self.ise_username, self.ise_password), headers=headers, data=payload, verify=False)
        if response.status_code != 201:
            output = f"\nError {response.status_code} {response.reason}! Endpoint '{endpoint.mac}' not created!"
        return output

    def createEndpointGroup(self, endpointGroup: EndpointGroup) -> str:
        """Create a new Endpoint Group.

        Args:
            endpointGroup (EndpointGroup): An Endpoint Group object

        Returns:
            str: Failed Endpoints
        """
        output: str = ""
        resource = f"{self.ise_url}/endpointgroup"
        headers = {
                    'Accept': 'application/json', 
                    'Content-Type': 'application/json'
                }
        payload = repr(endpointGroup)
        response = requests.post(resource, auth=(self.ise_username, self.ise_password), headers=headers, data=payload, verify=False)
        if response.status_code != 201:
            output = f"\nError {response.status_code} {response.reason}! Endpoint Group {endpointGroup.name} not created!"
        return output        


    def deleteEndpoint(self, endpoint: Endpoint) -> str:
        """Delete an endpoint.

        Args:
            endpoint (Endpoint): An Endpoint object

        Returns:
            str: Failed Endpoints
        """
        output: str = ""
        self.__checkEndpointID(endpoint)

        resource = f"{self.ise_url}/endpoint/{endpoint.id}"
        headers = {'Accept': 'application/json'}
        response = requests.delete(resource, auth=(self.ise_username, self.ise_password), headers=headers, verify=False)
        if response.status_code != 204:
            output = f"\nError {response.status_code} {response.reason}! Endpoint '{endpoint.mac}' not deleted!"
        return output

    def deleteEndpointGroup(self, endpointGroup: EndpointGroup) -> str:
        """Delete an Endpoint Group.

        Args:
            endpointGroup (EndpointGroup): An Endpoint Group object

        Returns:
            str: Failed Endpoint Groups
        """
        output: str = ""
        if endpointGroup.id == "":
            self.__populateEndpointGroupIDbyName(endpointGroup)
        
        resource = f"{self.ise_url}/endpointgroup/{endpointGroup.id}"
        headers = {'Accept': 'application/json'}
        response = requests.delete(resource, auth=(self.ise_username, self.ise_password), headers=headers, verify=False)
        if response.status_code != 204:
            output = f"\nError {response.status_code} {response.reason}! Endpoint Group '{endpointGroup.name}' not deleted!"
        return output

    def addEndpointToGroup(self, endpoint: Endpoint, endpointGroup: EndpointGroup) -> str:
        """Adds an Endpoint to an Endpoint Group. If no ID is set in the instances a lookup will be performed.

        Args:
            endpoint (Endpoint): An Endpoint object
            endpointGroup (EndpointGroup): An EndpointGroup object

        Returns:
            str: Failed Endpoints
        """
        output: str = ""
        self.__checkEndpointGroupID(endpointGroup)
        self.__checkEndpointID(endpoint)
        endpoint.setGroupID(endpointGroup.id)
        resource = f"{self.ise_url}/endpoint/{endpoint.id}"
        headers = {
                    'Accept': 'application/json', 
                    'Content-Type': 'application/json'
                }
        
        payload = json.dumps(endpoint.getGroupInfoJSON())
        response = requests.put(resource, auth=(self.ise_username, self.ise_password), headers=headers, data=payload, verify=False)
        if response.status_code != 200:
            output = f"\nError Endpoint {response.status_code} {response.reason}! Endpoint '{endpoint.mac}' not added to Group '{endpointGroup.name}'!"
        return output

    def __checkEndpointGroupID(self, endpointGroup: EndpointGroup):
        if endpointGroup.id == "":
            self.__populateEndpointGroupIDbyName(endpointGroup)
            
    def __checkEndpointID(self, endpoint):
        if endpoint.id == "":
            self.__populateEndpointIDbyName(endpoint)

    def __populateEndpointIDbyName(self, endpoint: Endpoint):
        """Retrieve the ID of an Endpoint.Name and set it in the specified object 

        Args:
            endpoint (Endpoint): An Endpoint object

        Raises:
            ValueError: If the Endpoint.Name can't be found
        """
        resource = f"{self.ise_url}/endpoint/name/{endpoint.name}"
        headers = {'Accept': 'application/json'}
        response = requests.get(resource, auth=(self.ise_username, self.ise_password), headers=headers, verify=False)
        if response.status_code == 200:
            jsondata = json.loads(response.text)
            endpoint.setID(jsondata["ERSEndPoint"]["id"])
        else:
            raise ValueError(f"\nError {response.status_code} {response.reason}! Endpoint-ID {endpoint.mac} not populated!")

    def __populateEndpointGroupIDbyName(self, endpointGroup: EndpointGroup):
        """Retrieve the ID of the "name"-attribute Endpoint Group and set it in the specified object

        Args:
            endpointGroup (EndpointGroup): An EndpointGroup object

        Raises:
            ValueError: If the EndpointGroup.Name can't be found
        """
        resource = f"{self.ise_url}/endpointgroup/name/{endpointGroup.name}"
        headers = {'Accept': 'application/json'}
        response = requests.get(resource, auth=(self.ise_username, self.ise_password), headers=headers, verify=False)
        if response.status_code == 200:
            jsondata = json.loads(response.text)
            endpointGroup.setID(jsondata["EndPointGroup"]["id"])
        else:
            raise ValueError(f"\nError {response.status_code} {response.reason}! Endpoint-ID {endpointGroup.name} not populated, check input!")
        
    def __getEndpointsFiltered(self, page: int, filter: Optional[str], filterOperator: Optional[FilterOperator] = FilterOperator.EQUALS):
        """Returns all Endpoints that match the filter. 
           The Search Results are paginated, thus a page parameter can be used to navigate through the search results.

        Args:
            page (int): A page number
            filter (Optional[str]): An optional filter for the "mac"-attribute.
            filterOperator (Optional[FilterOperator], optional): An ENUM of FilterOperator. Defaults to FilterOperator.EQUALS.

        Returns:
            Response: A response object
        """
        if filter != "" and isinstance(filterOperator, FilterOperator):
            resource = f"{self.ise_url}/endpoint?size=100&page={page}&filter=mac.{filterOperator.value}.{filter}"
        else:
          resource = f"{self.ise_url}/endpoint?size=100&page={page}"
        payload = {}
        headers = {'Accept': 'application/json'}
        return requests.get(resource, auth=(self.ise_username, self.ise_password), headers=headers, data=payload, verify=False)

    def __getEndpointMatchingGroupIDPaginated(self, page: int, groupID: str):
        """Retrieves all the Endpoints that match the given group ID

        Args:
            page (int): A page number
            groupID (str): A group ID of an Endpoint Group

        Returns:
            Response: A response object
        """
        resource = f"{self.ise_url}/endpoint?size=100&page={page}&filter=groupId.EQ.{groupID}" 
        payload = {}
        headers = {'Accept': 'application/json'}
        return requests.get(resource, auth=(self.ise_username, self.ise_password), headers=headers, data=payload, verify=False)

    def __getEndpointGroupsFiltered(self, page: int, filter: Optional[str], filterOperator: Optional[FilterOperator] = FilterOperator.EQUALS):
        """Retrieves all Endpoint groups that match the specified filter.

        Args:
            page (int): A page number
            filter (Optional[str]): An optional filter for the "mac"-attribute.
            filterOperator (Optional[FilterOperator], optional): An ENUM of FilterOperator. Defaults to FilterOperator.EQUALS.

        Returns:
            Response: A response object
        """
        if filter != "" and isinstance(filterOperator, FilterOperator):
            resource = f"{self.ise_url}/endpointgroup?size=100&page={page}&filter=name.{filterOperator.value}.{filter}"
        else:
          resource = f"{self.ise_url}/endpointgroup?size=100&page={page}"  
        payload = {}
        headers = {'Accept': 'application/json'}
        return requests.get(resource, auth=(self.ise_username, self.ise_password), headers=headers, data=payload, verify=False)

    def __getNextPageNumber(self, jsondata) -> int:
        """Extracts the next page number from a search result of a get-Request.
           The "next-page"-url is parsed and the page number extracted.
        Args:
            jsondata ([type]): A GET-Request containing a "SearchResult"-Key

        Returns:
            int: The next page number
        """
        page: int = -1
        if "nextPage" in jsondata["SearchResult"]:
            for queries in urlparse(jsondata["SearchResult"]["nextPage"]["href"]).query.split("&"):
                query = queries.split("=")
                if "page" in query:
                    page = query[1]
        return page
        


    
        
       