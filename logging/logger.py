import MySQLdb
import datetime

def logEvent(destIP, destPort, srcIP, srcPort, content):
	#connecting to Database
	db = MySQLdb.connect(host="localhost", user="root", passwd="akash", db="logs")

	#for interacting with the Database
	cur = db.cursor()

	#sanitizing the values
	destIP = db.escape_string(destIP)
	srcIP = db.escape_string(srcIP)
	content = db.escape_string(content)
	f = '%Y-%m-%d %H:%M:%S'
	time = datetime.datetime.now()
	time.strftime(f)

	#inserting the values into the table
	cur.execute("INSERT INTO LogData (Timestamp, Dest IP, Dest Port, Source IP, Source Port, Content) VALUES (%s, %s, %d, %s, %d, %s)", time, destIP, destPort, srcIP, srcPort, content)

	#closing the Database connection
	db.close()

def logSession():
	 #connecting to Database
        db = MySQLdb.connect(host="localhost", user="root", passwd="akash", db="logs")
	
	#for interacting with the Database
        cur = db.cursor()

        #sanitizing the values
        destIP = db.escape_string(destIP)
        srcIP = db.escape_string(srcIP)
        content = db.escape_string(content)
        f = '%Y-%m-%d %H:%M:%S'
        time = datetime.datetime.now()
        time.strftime(f)

        #inserting the values into the table
        cur.execute("INSERT INTO LogData (Timestamp, Dest IP, Dest Port, Source IP, Source Port, Content) VALUES (%s, %s, %d, %s, %d, %s)", time, destIP, destPort, srcIP, srcPort, content)

        #closing the Database connection
        db.close()	
