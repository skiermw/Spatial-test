# LoadCSVPol.py

from py2neo import neo4j
import csv
from string import Template

def main():

    

    # Start GraphDatabaseService and the batch writer.
    graph = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
    batch = neo4j.WriteBatch(graph)
     
##############
    # Load data from CSV into a list called policies.
    # pol_no, agent_no, line, ins_name, fam_no, status, tot_prem, tier, address, city, state
    
    csv_policies = []
     
    with open('policy.csv', 'rb') as file:
        reader = csv.reader(file, delimiter = '|', quotechar = '"')
        #next(reader, None) # Skip header row.
        for row in reader:
            csv_policies.append(row)
     
    # The i^th "row" of the policies list can be accessed through policies[i]:
    #print(csv_policies[0])
    # ['12345', '0000', 'Inactive', etc
     
    # The j^th "column" of the i^th "row" of the policies list can be accessed through policies[i][j]:
    #print(csv_policies[0][1])
    # United Kingdom
    
##############
    # Create Family nodes
    # Add uniqueness constraint.
    neo4j.CypherQuery(graph, "CREATE CONSTRAINT ON (f:Family) ASSERT f.number IS UNIQUE").run()
    
     
    # Put all policy  into a list called policies.
    families = []
     
    for i in range(0, len(csv_policies)):
        families.append(csv_policies[i][4].strip())
     
    # Convert list of family numbers to a set to get a unique set of values.
    families = set(families)
     
    # Create Family nodes.
    cypher = "MERGE (f:Family {number:{family_no}})"
     
    for family_no in families:
        params = dict(family_no = family_no)
        batch.append_cypher(cypher, params)
        #print 'family'
     
    batch.run()
    print 'Family done'

##############
    # Create Address nodes
    # Add uniqueness constraint.
    neo4j.CypherQuery(graph, "CREATE CONSTRAINT ON (a:Address) ASSERT a.address_key IS UNIQUE").run()
    
     
    # Put all policy  into a list called policies.
    addresses = []
     
    for i in range(0, len(csv_policies)):
        addresses.append(csv_policies[i][8].strip())
     
    # Convert list of family numbers to a set to get a unique set of values.
    addresses = set(addresses)
     
    # Create Family nodes.
    ak = Template('$a|$c|$s')
    cypher = "MERGE (a:Address {street:{address}, city:{city}, state:{state}, address_key:{address_key}})"
    
    #print 'params = %s' % params
    vars = ['address', 'city', 'state', 'address_key']



    # Execute in batches of 1000.
    BATCH_SIZE = 1000
    start = 0
    end = BATCH_SIZE
     
    for i, e in enumerate(csv_policies):
        #print 'e = %s' % e
        #print 'e[0] = %s' % e[0]
        params = dict(zip(vars, [e[8], e[9], e[10], ak.substitute(a=e[8], c=e[9], s=e[10])]))
        if i in range(start, end):
            #print cypher, params
            batch.append_cypher(cypher, params)
        else:
            batch.append_cypher(cypher, params)
            batch.run()
            print("Address Batch %s complete." % (end / BATCH_SIZE))
            start = end + 1
            end += BATCH_SIZE
     
    #batch.run()
    #for result in batch.stream():
     #   print 'a'
     
    batch.run()


    # Create Policy and Address nodes.
    # Add uniqueness constraint.
    neo4j.CypherQuery(graph, "CREATE CONSTRAINT ON (p:Policy) ASSERT p.number IS UNIQUE").run()
    
    
    
    cypher = "MATCH (f:Family {number:{family_no}}), (a:Address {address_key:{address_key}}) " \
             "MERGE (f)-[:HAS_POLICY]->(p:Policy {number:{pol_no}, agent_no:{agent_no}, line:{line}, ins_name:{ins_name}, status:{status}, tot_prem:{tot_prem}, tier:{tier}})" \
             "-[:LOCATED_AT]->(a)"
     
    vars = ['pol_no', 'agent_no', 'line', 'ins_name', 'family_no', 'status', 'tot_prem', 'tier', 'address', 'city', 'state', 'address_key']

    
    
    # Execute in batches of 1000.
    BATCH_SIZE = 1000
    start = 0
    end = BATCH_SIZE
     
    for i, e in enumerate(csv_policies):
        #print 'e = %s' % e
        #print 'e[0] = %s' % e[0]
        params = dict(zip(vars, [e[0], e[1], e[2], e[3], e[4].strip(), e[5], float(e[6]), e[7], e[8], e[9], e[10], ak.substitute(a=e[8], c=e[9], s=e[10])]))
        #print 'params = %s' % params
        if i in range(start, end):
            #print cypher, params
            batch.append_cypher(cypher, params)
        else:
            batch.append_cypher(cypher, params)
            batch.run()
            print("Policy Batch %s complete." % (end / BATCH_SIZE))
            start = end + 1
            end += BATCH_SIZE
     
    batch.run()
    #for result in batch.stream():
    #    print 'x'
    
    #print 'return = %s' % ret
    print("Batch %s complete." % (end / BATCH_SIZE))
    print("All done!")    
#############################################
if __name__=='__main__':
    main()
