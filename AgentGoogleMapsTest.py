# AgentGoogleMapsTest.py
from py2neo import neo4j, rel
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash



# configuration
QUERY = "MATCH (p:Policy {agent_no:' %s '})-[:LOCATED_AT]->(a) RETURN Distinct(a), a.lat AS lat, a.lng AS lng"
 
DEBUG = True
SECRET_KEY = 'development key'

start_job =""

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
#app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    try:
        graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
		
    except rest.ResourceNotFound:
        print 'Database service not found'
    return graph_db
		
		
@app.before_request
def before_request():
    graph_db = connect_db()

@app.route('/')
def show_addesses():
	agent_no = '6399'
	print 'agent_no is %s' % agent_no
	if agent_no <> '':
		query = QUERY % agent_no
				
		graph_db = connect_db()
		
		lat_lng_query = neo4j.CypherQuery(graph_db, query)
		
		geocodes = [dict(lat=result.lat, lng=result.lng) for result in lat_lng_query.stream()]
		
		
	else:
		geocodes = ""
		
	print 'geocodes = %s' % geocodes[0]
	
	print 'Num predessors %i' % len(geocodes)
	
	return render_template('show_65203_agent.html',geocodes=geocodes)

@app.route('/submit', methods=['POST'])
def submit_agent():
	global agent_no
	
	agent_no = "'%s'" % request.form['agent_no']
	flash('%s' % request.form['agent_no'])
	print 'agent is %s' % agent_no
	
	return redirect(url_for('show_addresses'))
	

if __name__ == '__main__':
    app.run(host='0.0.0.0')
	#app.run()
