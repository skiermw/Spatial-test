
import requests, csv


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
                'format': 'csv',
                'includeHeader': 'false',
                'notStore': 'true'
                }
                
        

        # Make the POST request here, passing body as the data:
        response = requests.post(url, body)
        return_data = response.text
        reader = csv.reader(return_data, delimiter=',')
        #print reader.next()
        for row in reader:
                print row
                
             
        
        print response
        print 'response status = %s' % response.status_code
        print 'response text = %s' % response.text
        
   
 
 
if __name__ == '__main__':
    main()	
	
	
######################################################################################	




