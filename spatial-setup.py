from neo4jrestclient.client import GraphDatabase
import json

def main():
	print 'spatial-setup.py starting...'
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
		#addresses = gdb.labels.create("Address")
		response = []
		mark = gdb.nodes.create(name="Mark Workman", street='5601 Majestic Circle', city='Columbia', state='MO', zip='65203', lat=38.891350, lon=-92.402642)
		
		# Create the Spatial Index
		return_val = gdb.extensions.SpatialPlugin.addSimplePointLayer(layer="geom", lat="lat", lon="lon")
		# Add the node created before to the index
		response = gdb.extensions.SpatialPlugin.addNodeToLayer(layer="geom", node=mark)
		
		nodes = gdb.extensions.SpatialPlugin.findGeometriesWithinDistance(layer="geom", pointX=38.89, pointY=-92.40, distanceInKm=100)
		print nodes
        
    
 
 
 
if __name__ == '__main__':
    main()	
	
	
######################################################################################	




