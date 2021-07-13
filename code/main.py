from RequestHandler.main.requesthandler import RequestHandler
"""
Author:         Gabriel Ben Abou @ Anyweb
Date:           29.04.2021
Version:        v1.0
Description:    
"""

if __name__ == '__main__':  
    requestHandler = RequestHandler()
    endpoints = requestHandler.getAllEndpoints()
    #endpointgroups = requestHandler.getAllEndpointGroups()
    print(f"Total Endpoints selected: {len(endpoints)}")
    #print(f"Total Endpointgroups selected: {len(endpointgroups)}")