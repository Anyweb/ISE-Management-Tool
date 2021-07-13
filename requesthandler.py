import requests
import json
import urllib3
from urllib.parse import urlparse
from dotenv import load_dotenv


"""
Author:         Gabriel Ben Abou @ Anyweb
Date:           09.07.2021
Version:        v1.0
Description:    XXXXXXXXXXXXXX
"""
urllib3.disable_warnings()

class RequestHandler:


    

    def getEndpointPaginated(page: int):
        url = f"https://isemgr-ise24.anyweb.ch:9060/ers/config/endpoint?size=100&page={page}"

        payload={}
        headers = {
            'Accept': 'application/json'
        }
        return requests.get(url, auth=('ERS_admin','ERS-passw0rd'), headers=headers, data=payload, verify=False)

    def getAllEndpoints():
        endpoints = {}
        page = 1
        while page != -1: 
            jsondata = json.loads(getEndpointPaginated(page).text)
            if "nextPage" in jsondata["SearchResult"]:
                for queries in urlparse(jsondata["SearchResult"]["nextPage"]["href"]).query.split("&"):
                    query = queries.split("=")
                    if "page" in query:
                        page = query[1]
            else:
                page = -1
            for endpoint in jsondata["SearchResult"]["resources"]:
                endpoints[endpoint["id"]] = endpoint["name"]    
        return endpoints

    
        
       