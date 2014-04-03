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
                'format': 'xml',
                'includeHeader': 'false',
                'notStore': 'true'
                }
                
        

        # Make the POST request here, passing body as the data:
        response = requests.post(url, body)
        print response
        print response.headers
        return_xml = response.text[3:]
        print return_xml
        
        geo_info = minidom.parseString(return_xml)
        
        lat = geo_info.getElementsByTagName('Latitude')
        lng = geo_info.getElementsByTagName('Longitude')
        print 'lat = %f  lng = %f' % {lat, lng}
   
 
 
if __name__ == '__main__':
    main()	
	
	
######################################################################################	




