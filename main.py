from isemanager import ISEManager

"""
Author:         Gabriel Ben Abou @ Anyweb
Date:           09.07.2021
Version:        v1.0
Description:    
"""

if __name__ == '__main__':
    manager = ISEManager() 
    endpoints = manager.getAllEndpoints()
    #print(f"Total Endpoints selected: {len(endpoints)}")
    #print(f"Total Endpointgroups selected: {len(endpointgroups)}")
