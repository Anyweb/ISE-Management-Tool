import unittest

from handler.isemanager import ISEManagerLight
from handler.requesthandler import RequestHandler, FilterOperator
from model.endpoint import Endpoint
from model.endpointgroup import EndpointGroup

class TestISEManager(unittest.TestCase):
    """
    This class is not a good example of unit-testing since it tests multiple methods and doesn't mock the ISE-API.
        ToDo: Unittest different classes instead of whole application
    """
    egs: list
    eg: EndpointGroup
    eps: list
    ep1: Endpoint
    ep2: Endpoint
    ep_mac_base = "00:11:22:33"
    manager: ISEManagerLight = ISEManagerLight()
    handler: RequestHandler = RequestHandler()

    def reset(self):
        self.egs = []
        self.eps = []
        self.eg = EndpointGroup(name="TestEPG15", description="Test Endpoint Group 1")
        self.ep1 = Endpoint(mac=f"{self.ep_mac_base}:04:07", description="Test Endpoint 1")
        self.ep2 = Endpoint(mac=f"{self.ep_mac_base}:04:17", description="Test Endpoint 2")
        self.egs.append(self.eg)
        self.eps.append(self.ep1)
        self.eps.append(self.ep2)

    
    def test_add_EPs_to_EPG(self):
        self.reset()
        # Create
        print(self.manager.createEndpointGroups(self.egs))
        print(self.manager.createEndpoints(self.eps))

        # Test
        for e in self.eps:
            self.assertEqual("", e.groupId)
        output_add = self.manager.addEndpointsToGroup(self.eps, self.eg)
        print(output_add)
        output_get_EP = self.handler.getEndpointsOfEndpointGroup(self.eg)
        for e in self.eps:
            self.assertEqual(self.eg.id, e.groupId)
    
        print(self.manager.getEndpointsOfEndpointGroup(self.eg))
        self.assertEqual("-- Add Endpoint(s) to Group: --\nProcessed 2 Endpoint(s).", output_add)
        self.assertEqual(2, len(output_get_EP))

        # Cleanup
        print(self.manager.deleteEndpointGroupsWithTheirEndpoints(self.egs))
        
    def test_remove_and_clear_EPG(self):
        self.reset()
        # Create and check creation
        print("1. Create: \n" + self.manager.createEndpointGroups(self.egs))
        print(self.manager.createEndpoints(self.eps))
        print(self.manager.addEndpointsToGroup(self.eps, self.eg))
        print("2. Check: \n" + self.manager.getEndpointsOfEndpointGroup(self.eg))
        
        print(self.manager.getAllEndpointGroups(filter=self.eg.name,filterOperator=FilterOperator.EQUALS))
        print(self.manager.getAllEndpoints(filter=self.ep_mac_base,filterOperator=FilterOperator.CONTAINS))

        get_eps_length = len(self.handler.getEndpointsOfEndpointGroup(self.eg))
        self.assertEqual(2, get_eps_length)
        
        # Test
        response = self.manager.deleteEndpointGroupsWithTheirEndpoints(self.egs)
        print("3. Delete and Clear: \n" + response)
        self.assertEqual("-- Remove Endpoint Group(s) with Endpoint(s): --\nProcessed 1 Endpoint Group(s) with a total of 4 Endpoint(s).", response)
        get_eps_length = len(self.handler.getEndpointsOfEndpointGroup(self.eg))
        self.assertEqual(0, get_eps_length)

        print("4. Verify: \n" + self.manager.getAllEndpointGroups(filter=self.eg.name,filterOperator=FilterOperator.EQUALS))
        print(self.manager.getAllEndpoints(filter=self.ep_mac_base,filterOperator=FilterOperator.CONTAINS))

if __name__ == '__main__':
    unittest.main()