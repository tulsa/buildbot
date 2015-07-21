from nose.tools import *
from unittest import TestCase

from buildbot.neo_flows import enhanced_GraphDatabase
from buildbot.data_schema import defined_relationships
from buildbot.data_schema import defined_nodes

neo4j_login = {
    "username" : "neo4j",
    "password" : "tulsa",
    "url" : "http://localhost:7474"
}

class test_neo4j_graph(TestCase):
    description = "UNITTEST -- delete when complete."
    
    def setUp(self):
        self.gdb = enhanced_GraphDatabase(**neo4j_login)
    
    def tearDown(self):
        q = '''
        MATCH (n)
        WHERE n.description="{}"
        OPTIONAL MATCH (n)-[r]-()
        DELETE n,r
        '''.format(self.description)
        
        result = self.gdb.query(q, data_contents=True)
        print result.stats["nodes_deleted"],
    
    def test_count_nodes(self):
        # Add a node and see if count is >= 1
        self.test_add_flow()
        assert(self.gdb.count_nodes() >= 1)

    def test_getitem(self):
        node = self.test_add_flow()
        idx  = node.id
        assert( self.gdb[idx]["metadata"]["id"] == idx )
    
    def test_add_flow(self):
        status_level = 0.7
        
        # Create a flow node, return the idx created.
        flow = defined_nodes["flow"]
        node = flow(description=self.description,status=status_level)

        # Add to the graph
        obj = self.gdb.add_node(node)

        # Make sure an ID has been assigned
        assert(node.id is not None)

        # Make sure data has been copied (check assigned status)
        assert(obj.data['status'] == status_level)
        
        return obj
    
    def test_add_flow_requires_job_relationship(self):
        time_cost = 7.8
        
        # Create the nodes
        v1 = defined_nodes["flow"](description=self.description)
        v2 = defined_nodes["job"](description=self.description)

        self.gdb.add_node(v1)
        self.gdb.add_node(v2)
        
        edge_func = defined_relationships[("flow","requires","job")]
        rel = edge_func(v1,v2,time=time_cost)

        # Add to the graph
        obj = self.gdb.add_relationship(rel)
        
        # Make sure an ID has been assigned
        assert(rel.id is not None)

        # Make sure data has been copied (check assigned status)
        assert(obj.properties['time'] == time_cost)

        return obj
    
    def test_remove_node_by_index(self):
        node = self.test_add_flow()
        stats = self.gdb.remove_node(node.id)
        assert(stats["nodes_deleted"] == 1)

    def test_remove_relationship_by_idx(self):
        rel = self.test_add_flow_requires_job_relationship()
        stats = self.gdb.remove_relationship(rel.id)
        assert(stats["relationship_deleted"] == 1)

    @raises(KeyError)
    def test_remove_missing_node(self):
        idx = self.test_add_flow().id
        self.gdb.remove_node(idx)
        self.gdb.remove_node(idx)

    @raises(KeyError)
    def test_remove_missing_edge(self):
        idx = self.test_add_flow_requires_job_relationship().id
        self.gdb.remove_relationship(idx)
        self.gdb.remove_relationship(idx)

'''
def test_flow_cost_propagation(): pass
'''