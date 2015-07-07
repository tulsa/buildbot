from nose import *
from unittest import TestCase

from buildbot_flows.neo_flows import enhanced_GraphDatabase
from buildbot_flows.data_nodes import flow

neo4j_login = {
    "username" : "neo4j",
    "password" : "tulsa",
    "url" : "http://localhost:7474"
}

class test_neo4j_graph(TestCase):
    def setUp(self):
        self.gdb = enhanced_GraphDatabase(**neo4j_login)
    
    def tearDown(self):
        print "This needs to delete all nodes authored by UNITTEST"
        pass

    '''        
    def test_add_flow(self):
        # Create a flow node, return the idx created.
        x = flow({"owner":"UNITTEST"})
        return self.gdb.add(flow)

    def test_remove_node_by_index(self):
        idx = self.test_add_flow()
        self.gdb.remove(idx)
    '''

'''

def test_create_flow():
    gdb.new_flow(description = "TEST FLOW")

def test_flow_flow_relationship(): pass
def test_flow_validation_relationship(): pass
def test_create_validation(): pass

def test_flow_count_nodes(): pass
def test_flow_count_relationships(): pass

def test_flow_select(): pass
def test_flow_export_json(): pass

def test_flow_cost_propagation(): pass
'''
