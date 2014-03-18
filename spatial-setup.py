from py2neo 	import neo4j, rel, node, cypher


def main():
	print 'spatial-setup.py starting...'
	graph_db = connect()
	load_db(graph_db)
        
def connect():
    try:
        #graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
        neo4j.authenticate("spatial.sb01.stations.graphenedb.com:24789/db/data/", "Spatial", "KLc3m79hDABiUZija6xv")

        graph_db = neo4j.GraphDatabaseService("http://Spatial:KLc3m79hDABiUZija6xv@spatial.sb01.stations.graphenedb.com:24789/db/data/")
        print 'graph_db= %s' % graph_db
    except rest.ResourceNotFound:
        print 'Database service not found'
    return graph_db
 
def load_db(graph_db):
        add_query = "CREATE (n:Address { street : '5601 Majestic Circle', city : 'Columbia', state : 'MO', zip : '65203'})"
        print 'In load_db()'
        create_query = neo4j.CypherQuery(graph_db, add_query)
        print 'create_query = %s' % create_query
        
    
 
 
 
if __name__ == '__main__':
    main()	
	
	
######################################################################################	




