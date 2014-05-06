# LoadGeoAddress.py
from xml.dom import minidom
import requests
from py2neo import neo4j
import collections
import csv
from string import Template
import datetime

def main():

    start_time = datetime.datetime.now().replace(microsecond=0)

    # Start GraphDatabaseService and the batch writer.
    graph = neo4j.GraphDatabaseService("http://10.8.30.5:7474/db/data/")
    batch = neo4j.WriteBatch(graph)
     

##############
    # Read unique Addess nodes for agent_no
    # Add uniqueness constraint.
    geocode_ct = 0
    agent_num = 'D637'
    address_query = "MATCH (p:Policy {agent_no:'%s'})-[:LOCATED_AT]->(a) RETURN DISTINCT(a)" % agent_num
    query = neo4j.CypherQuery(graph, address_query)
    
    for address in query.stream():
        address_node = address[0]
        #print address_node._id
        street = address_node["street"].strip()
        city = address_node["city"].strip()
        state = address_node["state"].strip()
        zip_code = address_node["zip"].strip()
        # check to see if lat/lng has already been added to this node
        if address_node["lat"]:
            print 'skipping' 
        else:
            geocode_ct = geocode_ct+1
            lat, lng = get_geo(street, city, state, zip_code)
            print address_node._id, lat, lng
            update_query = "START n=node(%s) SET n.lat = %s, n.lng = %s return n" % (address_node._id, lat, lng)
            neo4j.CypherQuery(graph, update_query).run()

    end_time = datetime.datetime.now().replace(microsecond=0)
    elapsed_time = end_time - start_time
    print 'Elapsed time: %s' % elapsed_time
    print 'total geocodes processed: %s' %geocode_ct
        
#####################
# use the Texas A&M geocode service with my apiKey
def get_geo(street, city, state, zip_code):
        url = 'http://geoservices.tamu.edu/Services/Geocode/WebService/GeocoderWebServiceHttpNonParsed_V04_01.aspx?'
        in_apiver = '4.01'
        in_apiKey = 'eb777451c4dc466c925b453b57bb1fef'
        in_street = street
        in_city = city
        in_state = state
        in_zip = zip_code
        #in_street = '5601 Majestic Circle'
        #in_city = 'Columbia'
        #in_state = 'MO'
        #in_zip = '65203'
        in_format = 'xml'
        body = {'apiKey': in_apiKey,
                'version': in_apiver,
                'streetAddress': in_street,
                'city': in_city,
                'state': in_state,
                'zip': in_zip,
                'allowTies': 'true',
                'tieBreakingStrategy':'',
                'census': 'false',
                'censusYear': '2010',
                'format': in_format,
                'includeHeader': 'false',
                'notStore': 'true'
                }
                
        

        # Make the POST request here, passing body as the data:
        response = requests.post(url, body)
       
        if response.status_code == requests.codes.ok:
                return_xml = response.text[3:]
                #print return_xml
                
                # parse returned xml
                geo_info = minidom.parseString(return_xml)

                # find the elements we are interested in
                lats = geo_info.getElementsByTagName('Latitude')
                lngs = geo_info.getElementsByTagName('Longitude')

                # get the values for these eleements
                for lat in lats:
                        #print 'Lat = %s' % lat.firstChild.nodeValue
                        latitude = lat.firstChild.nodeValue
                for lng in lngs:
                        #print 'Lng = %s' % lng.firstChild.nodeValue
                        longitude = lng.firstChild.nodeValue
        else:
                print 'POST FAILURE: Response code = %s' % response.status_code
                #response.raise_for_status()
                latitude = 0.0
                longitude = 0.0
                
        #print latitude, longitude
        return latitude, longitude
   
   
 
   
#############################################
if __name__=='__main__':
    main()
