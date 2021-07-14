import os
import requests
import json
import urllib3
from urllib.parse import urlparse
from typing import Optional
from dotenv import load_dotenv
from endpoint import Endpoint
from endpointgroup import EndpointGroup
from enum import Enum


"""
Author:         Gabriel Ben Abou @ Anyweb
Date:           09.07.2021
Version:        v1.0
Description:    XXXXXXXXXXXXXX
"""
urllib3.disable_warnings()

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
    ise_username: str
    ise_password: str
    ise_url: str

    def __init__(self):
        load_dotenv()
        self.ise_username = os.getenv('username')
        self.ise_password = os.getenv('password')
        self.ise_url = os.getenv('baseurl')

    def getAllEndpoints(self, filter: Optional[str], filterOperator: Optional[FilterOperator]):
        endpoints = [] 
        page = 1
        while page != -1: 
            jsondata = json.loads(self.__getEndpointsFiltered(page, filter, filterOperator).text)
            page = self.__getNextPageNumber(jsondata)
            for endpoint in jsondata["SearchResult"]["resources"]:
                endpoints.append(Endpoint(id=endpoint["id"],name=endpoint["name"]))
        return endpoints

    def getAllEndpointGroups(self, filter: Optional[str], filterOperator: Optional[FilterOperator]):
        endpointgroups = [] 
        page = 1
        while page != -1: 
            jsondata = json.loads(self.__getEndpointGroupsFiltered(page, filter, filterOperator).text)
            page = self.__getNextPageNumber(jsondata)
            for endpointgroup in jsondata["SearchResult"]["resources"]:
                endpointgroups.append(EndpointGroup(id=endpointgroup["id"],name=endpointgroup["name"],description=endpointgroup["description"]))
        return endpointgroups

    def getEndpointsOfEndpointGroup(self, endpointGroup: EndpointGroup):
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

    def createEndpoint(self, endpoint: Endpoint):
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

    def createEndpointGroup(self, endpointGroup: EndpointGroup):
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


    def deleteEndpoint(self, endpoint: Endpoint):
        output: str = ""
        if endpoint.id == "":
            self.__populateEndpointIDbyName(endpoint)

        resource = f"{self.ise_url}/endpoint/{endpoint.id}"
        headers = {'Accept': 'application/json'}
        response = requests.delete(resource, auth=(self.ise_username, self.ise_password), headers=headers, verify=False)
        if response.status_code != 204:
            output = f"\nError {response.status_code} {response.reason}! Endpoint '{endpoint.mac}' not deleted!"
        return output

    def deleteEndpointGroup(self, endpointGroup: EndpointGroup):
        output: str = ""
        if endpointGroup.id == "":
            self.__populateEndpointGroupIDbyName(endpointGroup)
        
        resource = f"{self.ise_url}/endpointgroup/{endpointGroup.id}"
        headers = {'Accept': 'application/json'}
        response = requests.delete(resource, auth=(self.ise_username, self.ise_password), headers=headers, verify=False)
        if response.status_code != 204:
            output = f"\nError {response.status_code} {response.reason}! Endpoint Group '{endpointGroup.name}' not deleted!"
        return output

    def addEndpointToGroup(self, endpoint: Endpoint, endpointGroup: EndpointGroup):
        output: str = ""
        if endpointGroup.id == "":
            self.__populateEndpointGroupIDbyName(endpointGroup)
        if endpoint.id == "":
            self.__populateEndpointIDbyName(endpoint)

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

    def __populateEndpointIDbyName(self, endpoint: Endpoint):
        resource = f"{self.ise_url}/endpoint/name/{endpoint.name}"
        headers = {'Accept': 'application/json'}
        response = requests.get(resource, auth=(self.ise_username, self.ise_password), headers=headers, verify=False)
        if response.status_code == 200:
            jsondata = json.loads(response.text)
            endpoint.setID(jsondata["ERSEndPoint"]["id"])
        else:
            raise ValueError(f"\nError {response.status_code} {response.reason}! Endpoint-ID {endpoint.mac} not populated!")

    def __populateEndpointGroupIDbyName(self, endpointGroup: EndpointGroup):
        resource = f"{self.ise_url}/endpointgroup/name/{endpointGroup.name}"
        headers = {'Accept': 'application/json'}
        response = requests.get(resource, auth=(self.ise_username, self.ise_password), headers=headers, verify=False)
        if response.status_code == 200:
            jsondata = json.loads(response.text)
            endpointGroup.setID(jsondata["EndPointGroup"]["id"])
        else:
            raise ValueError(f"\nError {response.status_code} {response.reason}! Endpoint-ID {endpointGroup.name} not populated, check input!")
        
    def __getEndpointsFiltered(self, page: int, filter: Optional[str], filterOperator: Optional[FilterOperator] = FilterOperator.EQUALS):
        if filter != "" and isinstance(filterOperator, FilterOperator):
            resource = f"{self.ise_url}/endpoint?size=100&page={page}&filter=mac.{filterOperator.value}.{filter}"
        else:
          resource = f"{self.ise_url}/endpoint?size=100&page={page}"
        payload = {}
        headers = {'Accept': 'application/json'}
        return requests.get(resource, auth=(self.ise_username, self.ise_password), headers=headers, data=payload, verify=False)

    def __getEndpointMatchingGroupIDPaginated(self, page: int, groupID: str):
        resource = f"{self.ise_url}/endpoint?size=100&page={page}&filter=groupId.EQ.{groupID}" 
        payload = {}
        headers = {'Accept': 'application/json'}
        return requests.get(resource, auth=(self.ise_username, self.ise_password), headers=headers, data=payload, verify=False)

    def __getEndpointGroupsFiltered(self, page: int, filter: Optional[str], filterOperator: Optional[FilterOperator] = FilterOperator.EQUALS):
        if filter != "" and isinstance(filterOperator, FilterOperator):
            resource = f"{self.ise_url}/endpointgroup?size=100&page={page}&filter=name.{filterOperator.value}.{filter}"
        else:
          resource = f"{self.ise_url}/endpointgroup?size=100&page={page}"  
        payload = {}
        headers = {'Accept': 'application/json'}
        return requests.get(resource, auth=(self.ise_username, self.ise_password), headers=headers, data=payload, verify=False)

    def __getNextPageNumber(self, jsondata):
        page: int = -1
        if "nextPage" in jsondata["SearchResult"]:
            for queries in urlparse(jsondata["SearchResult"]["nextPage"]["href"]).query.split("&"):
                query = queries.split("=")
                if "page" in query:
                    page = query[1]
        return page
        


    
        
       