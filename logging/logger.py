import MySQLdb
import datetime

def logEvent(destIP, destPort, srcIP, srcPort, content):
    #connecting to Database
    db = MySQLdb.connect(host="localhost", user="magbastard", passwd="MagnanimousBastard@CS460", db="MagBastard")

    #for interacting with the Database
    cur = db.cursor()

    #sanitizing the values
    destIP = db.escape_string(destIP)
    srcIP = db.escape_string(srcIP)
    content = db.escape_string(content)
    f = '%Y-%m-%d %H:%M:%S'
    time = datetime.datetime.now().strftime(f)

    #inserting the values into the table
   
    query = "INSERT INTO LogData (Timestamp, DestIP, DestPort, SourceIP, SourcePort, Content) VALUES ('%s', '%s', %d, '%s', %d, '%s')" % (time, destIP, destPort, srcIP, srcPort, content)
   
    cur.execute(query)
    db.commit()
   
    #closing the Database connection
    db.close()

def updateSession(ip,resp,p21=-1,p22=-1,p25=-1,p80=-1,p139=-1):
    #connecting to Database
    db = MySQLdb.connect(host="localhost", user="magbastard", passwd="MagnanimousBastard@CS460", db="MagBastard")
	
    #for interacting with the Database
    cur = db.cursor()

    ip = db.escape_string(ip)
    resp = db.escape_string(resp)
    f = '%Y-%m-%d %H:%M:%S'
    time = datetime.datetime.now().strftime(f)

    cur.execute("SELECT * FROM SessionData WHERE ip=%s", (ip,))
    if cur.fetchone():
	query = "UPDATE SessionData SET Timestamp='%s', Response='%s', P21=%d, P22=%d, P25=%d, P80=%d, P139=%d WHERE IP='%s'" % (time, resp, p21,p22,p25,p80,p139, ip)
        cur.execute(query)
    else:
        #inserting the values into the table
	query = "INSERT INTO SessionData (IP, Timestamp, Response, P21, P22, P25, P80, P139) VALUES ('%s', '%s', '%s', %d, %d, %d, %d, %d)" % (ip, time, resp, p21,p22,p25,p80,p139)
        cur.execute(query)

    #closing the Database connection
    db.commit()
    db.close()

def updateTimestamp(ip):
    #connecting to Database
    db = MySQLdb.connect(host="localhost", user="magbastard", passwd="MagnanimousBastard@CS460", db="MagBastard")
	
    #for interacting with the Database
    cur = db.cursor()

    ip = db.escape_string(ip)
    f = '%Y-%m-%d %H:%M:%S'
    time = datetime.datetime.now().strftime(f)

    cur.execute("UPDATE SessionData SET Timestamp=%s WHERE IP=%s", (time, ip))

    #closing the Database connection
    db.commit()
    db.close()

def retrieveSession(ip):
    #connecting to Database
    db = MySQLdb.connect(host="localhost", user="magbastard", passwd="MagnanimousBastard@CS460", db="MagBastard")
	
    #for interacting with the Database
    cur = db.cursor()

    ip = db.escape_string(ip)

    cur.execute("SELECT * FROM SessionData WHERE IP=%s", (ip,))
    session = cur.fetchone()
    db.close()
    
    if not session:
	return None

    timestamp = session[1]
    elapsed = datetime.datetime.now() - timestamp

    if(elapsed.seconds > 300):
	return None
 	
    return session
