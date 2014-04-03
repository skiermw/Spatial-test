from neo4jrestclient.client import GraphDatabase, Node
import json
import requests
import pprint

def main():
    print 'spatial-test-query.py starting...'
    graph_db = connect()
    load_db(graph_db)
        
def connect():
    try:
        #graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
                url = "http://Spatial:KLc3m79hDABiUZija6xv@spatial.sb01.stations.graphenedb.com:24789/db/data/"
        #neo4j.authenticate("spatial.sb01.stations.graphenedb.com:24789/db/data/", "Spatial", "KLc3m79hDABiUZija6xv")

                graph_db = GraphDatabase(url, username="Spatial", password="KLc3m79hDABiUZija6xv")
                print 'graph_db= %s' % graph_db
    except rest.ResourceNotFound:
        print 'Database service not found'
    return graph_db
 
def load_db(gdb):
        """
        # Create nodes with geo data
        mark = gdb.nodes.create(name="Mark Workman", street='5601 Majestic Circle', city='Columbia', state='MO', zip='65203', lat=38.891350, lon=-92.402642)
        teresa = gdb.nodes.create(name="Teresa Magruder", street='4704 Silver Cliff Dr.', city='Columbia', state='MO', zip='65203', lat=38.896138, lon=-92.404702)
        frank = gdb.nodes.create(name="Frank Thompson", street='4500 Thornbrook Ter.', city='Columbia', state='MO', zip='65203', lat=38.888766, lon=-92.403622)
        todd = gdb.nodes.create(name="Todd Thompson", street='6900 Seminole Ct.', city='Columbia', state='MO', zip='65203', lat=38.872152, lon=-92.395562)
        
        # Create the Point layer
        return_val = gdb.extensions.SpatialPlugin.addSimplePointLayer(layer="address", lat="lat", lon="lon")
        
        # Create Spatial Index
        Address_Index = gdb.nodes.indexes.create("addressIndex",  provider="spatial", geometry_type="point", lat="lat", lon="lon")
        print Address_Index
        
        # Add the nodes created before to the index
        answer = Address_Index.add("key", "value", mark)
        answer = Address_Index.add("key", "value", teresa)
        answer = Address_Index.add("key", "value", frank)
        answer = Address_Index.add("key", "value", todd)
        """
                # this cypher query works
                # start node = node:addressIndex('withinDistance:[38.89,-92.40, 1.0]') return node
                # but this doesn't
        layer = gdb.extensions.SpatialPlugin.getLayer( layer="address")
        #for node in layer:
        #    print node.layer
        Node.index_node = layer.next()
        print "layer = %s" % Node.index_node
        nodes = gdb.extensions.SpatialPlugin.findGeometriesWithinDistance( pointX='38.89', pointY='-92.40', distanceInKm='1.0', layer="address")
        print "nodes = %s" % nodes
        query_parms = { 'layer': 'address',
                        'pointX': 38.89,
                        'pointY': -92.40,
                        'distanceInKm': 1.0
                        }
        endpoint = 'http://Spatial:KLc3m79hDABiUZija6xv@spatial.sb01.stations.graphenedb.com:24789/db/data/ext/SpatialPlugin/graphdb/findGeometriesWithinDistance'
        response = requests.post( endpoint, params=query_parms)
        print 'response = %s' % response
        data = response.json
        pprint.pprint(data)
        query = "start node = node:addressIndex('withinDistance:[38.89,-92.40, 1.0]') return node"
        result = gdb.query(query, returns=(Node))
        print 'Query results: %s' % result
        mark = result[0]  
        print mark
        
        
 
 
if __name__ == '__main__':
    main()  
    
    
######################################################################################  




