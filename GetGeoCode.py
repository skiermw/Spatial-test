from xml.dom import minidom
import requests


def main():
        url = 'http://geoservices.tamu.edu/Services/Geocode/WebService/GeocoderWebServiceHttpNonParsed_V04_01.aspx?'
        in_apiver = '4.01'
        in_apiKey = 'eb777451c4dc466c925b453b57bb1fef'
        in_street = '5601 Majestic Circle'
        in_city = 'Columbia'
        in_state = 'MO'
        in_zip = '65203'
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
                        print 'Lat = %s' % lat.firstChild.nodeValue
                for lng in lngs:
                        print 'Lng = %s' % lng.firstChild.nodeValue
        else:
                print 'POST FAILURE: Response code = %s' % response.status_code
                #response.raise_for_status()
   
   
 
 
if __name__ == '__main__':
    main()	
	
	
######################################################################################	




