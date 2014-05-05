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
    cur.execute("INSERT INTO LogData (Timestamp, Dest IP, Dest Port, Source IP, Source Port, Content) VALUES (%s, %s, %d, %s, %d, %s)", time, destIP, destPort, srcIP, srcPort, content)

    #closing the Database connection
    db.close()

def updateSession(ip,p21=-1,p22=-1,p25=-1,p80=-1,p139=-1):
    #connecting to Database
    db = MySQLdb.connect(host="localhost", user="root", passwd="akash", db="logs")
	
    #for interacting with the Database
    cur = db.cursor()

    ip = db.escape_string(ip)
    f = '%Y-%m-%d %H:%M:%S'
    time = datetime.datetime.now().strftime(f)

    #inserting the values into the table
    cur.execute("INSERT INTO SessionData (Timestamp, ip, p21, p22, p25, p80, p139) VALUES (%s, %d, %d, %d, %d, %d)", time, ip, p21,p22,p25,p80,p139)

    #closing the Database connection
    db.close()

def logSession(ip,p21=-1,p22=-1,p25=-1,p80=-1,p139=-1):
    #connecting to Database
    db = MySQLdb.connect(host="localhost", user="magbastard", passwd="MagnanimousBastard@CS460", db="MagBastard")
	
    #for interacting with the Database
    cur = db.cursor()

    ip = db.escape_string(ip)
    f = '%Y-%m-%d %H:%M:%S'
    time = datetime.datetime.now().strftime(f)

    #inserting the values into the table
    cur.execute("INSERT INTO SessionData (Timestamp, ip, p21, p22, p25, p80, p139) VALUES (%s, %d, %d, %d, %d, %d)", time, ip, p21,p22,p25,p80,p139)

    #closing the Database connection
    db.close()
