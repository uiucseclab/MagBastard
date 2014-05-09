import MySQLdb
import datetime

timeout = 300 # seconds
timestampFormatString = '%Y-%m-%d %H:%M:%S.%f'

class Session:
    def __init__(self, ip='', ts=datetime.datetime.now(), ftp=-1,ssh=-1,smtp=-1,http=-1,samba=-1,pts={}):
        self.IP = ip
        self.Timestamp = ts
        self.Ports = pts
        if ftp != -1:
            self.Ports['ftp'] = ftp
        if ssh != -1:
            self.Ports['ssh'] = ssh
        if smtp != -1:
            self.Ports['smtp'] = smtp
        if http != -1:
            self.Ports['http'] = http
        if samba != -1:
            self.Ports['samba'] = samba
        

def logEvent(destIP, destPort, srcIP, srcPort, content):
    #connecting to Database
    db = MySQLdb.connect(host="localhost", user="magbastard", passwd="MagnanimousBastard@CS460", db="MagBastard")

    #for interacting with the Database
    cur = db.cursor()

    #sanitizing the values
    destIP = db.escape_string(destIP)
    srcIP = db.escape_string(srcIP)
    content = db.escape_string(content)
    f = timestampFormatString
    time = datetime.datetime.now().strftime(f)

    #inserting the values into the table
   
    query = "INSERT INTO LogData (Timestamp, DestIP, DestPort, SourceIP, SourcePort, Content) VALUES ('%s', '%s', %d, '%s', %d, '%s')" % (time, destIP, destPort, srcIP, srcPort, content)
   
    cur.execute(query)
    db.commit()
   
    #closing the Database connection
    db.close()

def updateSession(ip,session=None):
    if session and not ip:
        ip = session.IP
    if not ip:
        return
    p21 = session.Ports['ftp'] if (session and 'ftp' in session.Ports) else -1
    p22 = session.Ports['ssh'] if (session and 'ssh' in session.Ports) else -1
    p25 = session.Ports['smtp'] if (session and 'smtp' in session.Ports) else -1
    p80 = session.Ports['http'] if (session and 'http' in session.Ports) else -1
    p139 = session.Ports['samba'] if (session and 'samba' in session.Ports) else -1

    #connecting to Database
    db = MySQLdb.connect(host="localhost", user="magbastard", passwd="MagnanimousBastard@CS460", db="MagBastard")
	
    #for interacting with the Database
    cur = db.cursor()

    ip = db.escape_string(ip)
    resp = db.escape_string(resp)
    f = timestampFormatString
    time = datetime.datetime.now()
    if session:
        session.Timestamp = time
    time = time.strftime(f)

    cur.execute("SELECT * FROM SessionData WHERE ip=%s", (ip,))
    if cur.fetchone():
	query = "UPDATE SessionData SET Timestamp='%s', Response='%s', P21=%d, P22=%d, P25=%d, P80=%d, P139=%d WHERE IP='%s'" % (time, '', p21,p22,p25,p80,p139, ip)
        cur.execute(query)
    else:
        #inserting the values into the table
	query = "INSERT INTO SessionData (IP, Timestamp, Response, P21, P22, P25, P80, P139) VALUES ('%s', '%s', '%s', %d, %d, %d, %d, %d)" % (ip, time, '', p21,p22,p25,p80,p139)
        cur.execute(query)

    #closing the Database connection
    db.commit()
    db.close()

def updateTimestamp(ip=None,session=None):
    if ip==None:
        if session:
            ip = session.IP
        else:
            return
    #connecting to Database
    db = MySQLdb.connect(host="localhost", user="magbastard", passwd="MagnanimousBastard@CS460", db="MagBastard")
	
    #for interacting with the Database
    cur = db.cursor()

    ip = db.escape_string(ip)
    f = timestampFormatString
    time = datetime.datetime.now()
    if session:
        session.Timestamp = time
    time = time.strftime(f)

    cur.execute("UPDATE SessionData SET Timestamp=%s WHERE IP=%s", (time, ip))
    response = cur.fetchone()
    if response:
        print(response)

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

    if(elapsed.seconds > timeout):
        return None

    ses = Session(ip=session[0],ts=session[1],resp=None,ftp=int(session[3]),ssh=int(session[4]),smtp=int(session[5]),http=int(session[6]),samba=int(session[7]))
    return ses
