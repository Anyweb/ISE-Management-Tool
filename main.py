import argparse
import os, sys

from model.endpoint import Endpoint
from model.endpointgroup import EndpointGroup
from handler.isemanager import ISEManagerLight
from handler.requesthandler import FilterOperator

"""
Author:         Gabriel Ben Abou @ Anyweb
Date:           09.07.2021
Version:        v1.0
Description:    
"""
   
def check_env_file():
    if not os.path.exists('.env'):
        print("""
        No .env File found, please use following scheme:
        -------------------------------------------------------------
            username="myUser"
            password="mySecretPassword"
            baseurl="https://isemgr-ise24.anyweb.ch:9060/ers/config"
        """)
        sys.exit()

def create_endpoint(name: str, mac: str, description: str) -> str:
    eps = []
    eps.append(Endpoint(name=name, mac=mac, description=description))
    print(manager.createEndpoints(eps))
    
def delete_endpoint(mac: str) -> str:
    print("Selected following Endpoints: ")
    print(manager.deleteEndpoints(find_endpoint(mac, FilterOperator.EQUALS)))

def create_endpointgroup(name: str, description: str) -> str:
    egs = []
    egs.append(EndpointGroup(name=name, description=description))
    print(manager.createEndpointGroups(egs))

def delete_endpointgroup(name: str) -> str:
    print("Selected following Endpoint Groups: ")
    print(manager.deleteEndpointGroups(find_endpointgroup(name, FilterOperator.EQUALS)))

def find_endpointgroup(filter: str, filterOperator: FilterOperator) -> list:
    return manager.getAllEndpointGroups(filter=filter, filterOperator=filterOperator)

def find_endpoint(filter: str, filterOperator: FilterOperator) -> list:
    return manager.getAllEndpoints(filter=filter, filterOperator=filterOperator)

def find_endpoints_of_endpointgroup(endpointgroup: EndpointGroup):
    return manager.getEndpointsOfEndpointGroup(endpointgroup)

def remove_endpointgroup(name: str):
    return manager.deleteEndpointGroupsWithTheirEndpoints(find_endpointgroup(name, FilterOperator.EQUALS))

def input_to_FilterOperator(input: str) -> FilterOperator: 
    return None
    
def setup_argparser():
    argument_parser = argparse.ArgumentParser(description="🤠 ISE-Manager Light used to create, delete, search Endpoints and Endpoint Groups. And a lot more!")
    argument_parser.add_argument('--name',help="Specify a name for Endpoints/Group.",type=str)
    argument_parser.add_argument('--mac',help="Specify a MAC-Address for Endpoint.",type=str)
    argument_parser.add_argument('--description',help="Specify a Description for Endpoint/Group.",type=str)
    argument_parser.add_argument('--filter-operator',help="Possible choices are: [EQUALS, NOT_EQUALS, STARTS_WITH, NOT_STARTS_WITH, ENDS_WITH, NOT_ENDS_WITH, CONTAINS, NOT_CONTAINS] Has to be used in conjunction with '--name' (for EndpointGroups) or '--mac' (for Endpoints). Defaults to EQUALS.",type=str, default="EQUALS")
    argument_parser.add_argument('--lookup',help="🔍 [SEARCH] Find an Endpoint Group with it's Endpoints (using '--name') or an Endpoint (using '--mac'). Can be used in conjunction with '--filter-operator'", action='store_true')
    argument_parser.add_argument('--create',help="✏️ [CREATE] Create an Endpoint Group (using '--name' and '--description') or an Endpoint (using '--mac' and '--description').", action='store_true')
    #argument_parser.add_argument('--assign',help="✏️ [ASSIGN] Assign an Endpoint (using '--mac') to an Endpoint Group (using '--id').", action='store_true')
    argument_parser.add_argument('--delete',help="🗑️ [DELETE] Delete an Endpoint Group (using '--name') or an Endpoint (using '--mac').", action='store_true')
    argument_parser.add_argument('--delete-with-clear',help="🗑️ [DELETE] Delete an Endpoint Group (using '--name') and all of it's Endpoints. Can be used in conjunction with '--filter-operator'.", action='store_true')   
    argument_parser.add_argument('--dry-run',help="🏍️ Show what Endpoints and Groups are involved witout performing the action", action='store_true')   
    args = argument_parser.parse_args()
    return args

def perform_lookup(args):
    # ToDo: FilterOperator conversion
    if args.name is not None and args.mac is None:
            egs = find_endpointgroup(args.name, FilterOperator.CONTAINS)
            # ToDo print endpoints per Group
            for eg in egs:
                find_endpoints_of_endpointgroup(eg)

    elif args.mac is not None and args.name is None:
        find_endpoint(args.mac, FilterOperator.CONTAINS)
    else:
        print("Only specify either --name (Endpoint Group) or --mac (Endpoint) for '--lookup'")

def perform_create(args):
    if args.name is not None and args.description is not None:
        if args.mac is not None:
            if not args.dry_run:
                create_endpoint(args.name, args.mac, args.description)
            else:
                print("The following Endpoint will be created:\n" + repr(Endpoint(name=args.name, mac=args.mac, description=args.description)))
        else:
            if not args.dry_run:
                create_endpointgroup(args.name, args.description)
            else:
                print("The following Endpoint Group will be created:\n" + repr(EndpointGroup(name=args.name, description=args.description)))
    else:
        print("For a create --name and --description are needed to create an Endpoint/Group. If an Endpoint is wanted --mac has to be added. For '--create'")

def perform_delete(args):
    if args.mac is not None and args.name is None:
        if not args.dry_run:
            delete_endpoint(args.mac)
        else:
            print("The following Endpoints would have been deleted:")
            find_endpoint(args.mac, FilterOperator.CONTAINS)
    if args.mac is None and args.name is not None:
        if not args.dry_run:
            delete_endpointgroup(args.name)
        else:
            print("The following Endpoint Groups would have been deleted:")
            find_endpointgroup(args.name, FilterOperator.CONTAINS)
        

def perform_delete_with_clear(args):
    if args.name is not None:
        if not args.dry_run:
            remove_endpointgroup(args.name)
        else:
            print("The following Endpoint Groups would have been deleted:")
            egs = find_endpointgroup(args.name, FilterOperator.CONTAINS)
            print("The following Endpoints would have been deleted:")
            for eg in egs:
                find_endpoints_of_endpointgroup(eg)
        

if __name__ == '__main__':
    check_env_file()
    manager = ISEManagerLight()
    args = setup_argparser()
    if args.dry_run:
        print("----DRY-RUN----")
    if args.name is not None or args.mac is not None:
        if args.lookup:
            perform_lookup(args)
        elif args.create:
            perform_create(args)
        elif args.delete:
            perform_delete(args)
        elif args.delete_with_clear:
            perform_delete_with_clear(args)
        else:
            print("Please choose an action. Check with '--help'")
    else:
        print("Error missing Name or MAC! Check with '--help'")
        sys.exit()

    #print(args)
    

    