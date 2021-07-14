import os
import requests
import json
import urllib3
from urllib.parse import urlparse
from dotenv import load_dotenv
from endpoint import Endpoint
from endpointgroup import EndpointGroup


"""
Author:         Gabriel Ben Abou @ Anyweb
Date:           09.07.2021
Version:        v1.0
Description:    XXXXXXXXXXXXXX
"""
urllib3.disable_warnings()

class RequestHandler:
    ise_username: str
    ise_password: str
    ise_url: str

    def __init__(self):
        load_dotenv()
        self.ise_username = os.getenv('username')
        self.ise_password = os.getenv('password')
        self.ise_url = os.getenv('baseurl')

    def getAllEndpoints(self):
        endpoints = [] 
        page = 1
        while page != -1: 
            jsondata = json.loads(self.__getEndpointPaginated(page).text)
            page = self.__getNextPageNumber(jsondata)
            for endpoint in jsondata["SearchResult"]["resources"]:
                endpoints.append(Endpoint(id=endpoint["id"],name=endpoint["name"]))
        return endpoints

    def getAllEndpointGroups(self):
        endpointgroups = [] 
        page = 1
        while page != -1: 
            jsondata = json.loads(self.__getEndpointGroupPaginated(page).text)
            page = self.__getNextPageNumber(jsondata)
            for endpointgroup in jsondata["SearchResult"]["resources"]:
                endpointgroups.append(Endpoint(id=endpointgroup["id"],name=endpointgroup["name"],description=endpointgroup["description"]))
        return endpointgroups

    def getEndpointsOfEndpointGroup(self, endpointGroup: EndpointGroup):
        groupID = endpointGroup.id
        endpoints = []
        page = 1
        while page != -1: 
            jsondata = json.loads(self.__getEndpointMatchingGroupIDPaginated(page, groupID).text)
            page = self.__getNextPageNumber(jsondata)
            for endpoint in jsondata["SearchResult"]["resources"]:
                endpoints.append(Endpoint(id=endpoint["id"],name=endpoint["name"]))
        return endpoints

    def createEndpoint(self, endpoint: Endpoint):
        resource = f"{self.ise_url}/endpoint"
        headers = {
                    'Accept': 'application/json', 
                    'Content-Type': 'application/json'
                }
        payload = {
            "ERSEndPoint" : {
                "id" : endpoint.id,
                "description" : endpoint.description,
                "mac" : endpoint.mac,
                "name" : endpoint.name
            }
        }
        payload = json.dumps(payload)
        response = requests.post(resource, auth=(self.ise_username, self.ise_password), headers=headers, data=payload, verify=False)
        if response.status_code == 201:
            return f"Endpoint {endpoint.mac} successfully created!"
        else:
            return f"Error {response.status_code} {response.reason}! Endpoint {endpoint.mac} not created!"

    def deleteEndpoint(self, endpoint: Endpoint):
        if endpoint.id == "":
            self.__populateEndpointIDbyName(endpoint)

        resource = f"{self.ise_url}/endpoint/{endpoint.id}"
        headers = {'Accept': 'application/json'}
        response = requests.delete(resource, auth=(self.ise_username, self.ise_password), headers=headers, verify=False)
        if response.status_code == 204:
            return f"Endpoint {endpoint.mac} successfully deleted!"
        else:
            return f"Error {response.status_code} {response.reason}! Endpoint {endpoint.mac} not deleted!"

    def __populateEndpointIDbyName(self, endpoint: Endpoint):
        resource = f"{self.ise_url}/endpoint/name/{endpoint.name}"
        headers = {'Accept': 'application/json'}
        response = requests.get(resource, auth=(self.ise_username, self.ise_password), headers=headers, verify=False)
        if response.status_code == 200:
            jsondata = json.loads(response.text)
            endpoint.setID(jsondata["ERSEndPoint"]["id"])
        else:
            return f"Error {response.status_code} {response.reason}! Endpoint-ID {endpoint.mac} not populated!"
        
    def __getEndpointPaginated(self, page: int):
        resource = f"{self.ise_url}/endpoint?size=100&page={page}"
        payload = {}
        headers = {'Accept': 'application/json'}
        return requests.get(resource, auth=(self.ise_username, self.ise_password), headers=headers, data=payload, verify=False)

    def __getEndpointMatchingGroupIDPaginated(self, page: int, groupID: str):
        resource = f"{self.ise_url}/endpoint?size=100&page={page}&filter=groupId.EQ.{groupID}"
        payload = {}
        headers = {'Accept': 'application/json'}
        return requests.get(resource, auth=(self.ise_username, self.ise_password), headers=headers, data=payload, verify=False)

    def __getEndpointGroupPaginated(self, page: int):
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
        


    
        
       