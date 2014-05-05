import MySQLdb
import datetime

def class session:
    def __init__():
        self.timestamp = datetime.datetime.now()
        self.services = {
            21: None,
            22: None,
            25: None,
            80: None,
            139: None
        }

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
    db = MySQLdb.connect(host="localhost", user="root", passwd="akash", db="logs")
	
    #for interacting with the Database
    cur = db.cursor()

    ip = db.escape_string(ip)
    resp = db.escape_string(resp)
    f = '%Y-%m-%d %H:%M:%S'
    time = datetime.datetime.now().strftime(f)

    cur.execute("SELECT * FROM SessionData WHERE ip=%s", (ip,))
    if cur.fetchone():
        cur.execute("UPDATE SessionData SET Timestamp=%s, Response=%s, P21=%s, P22=%s, P25=%s, P80=%s, P139=%s WHERE IP=%s", (time, resp, p21,p22,p25,p80,p139, ip))
    else:
        #inserting the values into the table
        cur.execute("INSERT INTO SessionData (IP, Timestamp, Response, P21, P22, P25, P80, P139) VALUES (%s, %d, %d, %d, %d, %d)", (ip, time, resp, p21,p22,p25,p80,p139))

    #closing the Database connection
    db.close()

def updatetimestamp(ip):
    #connecting to Database
    db = MySQLdb.connect(host="localhost", user="root", passwd="akash", db="logs")
	
    #for interacting with the Database
    cur = db.cursor()

    ip = db.escape_string(ip)
    f = '%Y-%m-%d %H:%M:%S'
    time = datetime.datetime.now().strftime(f)

    cur.execute("UPDATE SessionData SET Timestamp=%s WHERE IP=%s", (time, ip))

    #closing the Database connection
    db.close()

def retrievesession(ip):
    #connecting to Database
    db = MySQLdb.connect(host="localhost", user="root", passwd="akash", db="logs")
	
    #for interacting with the Database
    cur = db.cursor()

    ip = db.escape_string(ip)

    cur.execute("SELECT * FROM SessionData WHERE IP=%s", (ip,))
    session = cur.fetchone()
    db.close()
    return session
