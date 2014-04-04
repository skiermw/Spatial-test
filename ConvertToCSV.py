#  ConvertToCSV.py - converts file from DB/2 (fixed format) to csv file
#
import  csv, socket, struct, time, sys

	


def main():
	
        load_file()
         
def load_file():
        db2file = 'pol-65203-pol01.txt'
        csvfile = 'pol-65203-pol01.csv'
        layout = [
                ( 'junk', 0, 2),
                ( 'pol_no', 2, 17 ),
                ( 'agent_no', 19, 10 ),
                ( 'line', 29, 8 ),
                ( 'ins_name', 37, 61 ),
                ( 'family', 98, 10 ),
                ( 'status', 108, 9 ),
                ( 'total_prem', 117, 17 ),
                ( 'tier', 134, 8 ),
                ( 'ins_street', 142, 31 ),
                ( 'ins_city', 173, 21 ),
                ( 'ins_state', 194, 9 )
       ]
        
        reclen= 205
        
        cobolFile= file( db2file, 'rb' )
        
        for recBytes in yieldRecords(cobolFile, reclen):
                record = dict()
                for name, start, size in layout:
                        record[name]= recBytes[start:start+size]
                        #print 'Record name = %s' % record[name]

                #print 'record = %s' % record
                print "list(record.values()) = %s" % list(record.values())
                
                with open('eggs.csv', 'wb') as csvfile:
                        csvwriter = csv.writer(csvfile, delimiter='|') 
                        csvwriter.writerows(list(record.values()))
               
def yieldRecords( aFile, recSize ):
        recBytes= aFile.read(recSize)
        while recBytes:
                yield recBytes
                recBytes= aFile.read(recSize)
                print recBytes


'''                
            if len(rowbuffer) >= bsize:
                load_batch(rowbuffer, gdb)
                rowbuffer = []
 
        if len(rowbuffer) > 0:
            load_batch(rowbuffer, gdb)
''' 
''' 
def load_batch(rows, graph_db):
 
        print "loading %i rows..." % len(rows)
        batch = neo4j.WriteBatch(graph_db)  # batch is linked to graph database
	
        for row in rows:
                pred, succ = row
		#print "%s %s" % (pred, succ)
		for pred_node in graph_db.find('Job', 'jobname', pred):
			
			print 'pred_node name is %s' % pred_node["jobname"]
		for succ_node in graph_db.find("Job", 'jobname', succ):
			print 'succ_node name is %s' % succ_node["jobname"]

		batch.create(rel(pred_node, "SUCCESSOR", succ_node))
    print 'Ok'
    batch.run()
 
    
''' 
 
if __name__ == '__main__':
    main()

######################################################################################	




