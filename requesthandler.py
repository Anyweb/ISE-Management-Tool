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

    def getEndpointPaginated(self, page: int):
        resource = f"{self.ise_url}/endpoint?size=100&page={page}"
        payload={}
        headers = {'Accept': 'application/json'}
        return requests.get(resource, auth=(self.ise_username, self.ise_password), headers=headers, data=payload, verify=False)

    def getAllEndpoints(self):
        endpoints = [] # ToDo: list of Endpoint-Objects
        page = 1
        while page != -1: 
            jsondata = json.loads(self.getEndpointPaginated(page).text)
            page = self.__getNextPageNumber(jsondata)
            for endpoint in jsondata["SearchResult"]["resources"]:
                endpoints.append(Endpoint(id=endpoint["id"],name=endpoint["name"]))
        return endpoints


    def __getNextPageNumber(self, jsondata):
        page: int = -1
        if "nextPage" in jsondata["SearchResult"]:
            for queries in urlparse(jsondata["SearchResult"]["nextPage"]["href"]).query.split("&"):
                query = queries.split("=")
                if "page" in query:
                    page = query[1]
        return page
        


    
        
       