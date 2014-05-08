import MySQLdb
import datetime

class Session:
    def __init__(self, ip='', ts=datetime.datetime.now(), resp='',p21=-1,p22=-1,p25=-1,p80=-1,p139=-1,pts={}):
        self.IP = ip
        self.Timestamp = ts
        self.Response = resp
        self.Ports = pts
        if not p21 == -1:
            self.Ports['P21'] = p21
        if not p22 == -1:
            self.Ports['P22'] = p22
        if not p25 == -1:
            self.Ports['P25'] = p25
        if not p80 == -1:
            self.Ports['P80'] = p80
        if not p139 == -1:
            self.Ports['P139'] = p139
        

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

def updateSession(ip='',session=None,resp='',p21=-1,p22=-1,p25=-1,p80=-1,p139=-1):
    if session:
        if not ip:
            ip = session.IP
        if not resp:
            resp = session.Response
        if p21==-1:
            if 'P21' in session.Ports:
                p21 = session.Ports['P21']
        if p22==-1:
            if 'P22' in session.Ports:
                p22 = session.Ports['P22']
        if p25==-1:
            if 'P25' in session.Ports:
                p25 = session.Ports['P25']
        if p80==-1:
            if 'P80' in session.Ports:
                p80 = session.Ports['P80']
        if p139==-1:
            if 'P139' in session.Ports:
                p139 = session.Ports['P139']
    if not ip:
        return
    #connecting to Database
    db = MySQLdb.connect(host="localhost", user="magbastard", passwd="MagnanimousBastard@CS460", db="MagBastard")
	
    #for interacting with the Database
    cur = db.cursor()

    ip = db.escape_string(ip)
    resp = db.escape_string(resp)
    f = '%Y-%m-%d %H:%M:%S'
    time = datetime.datetime.now()
    if session:
        session.Timestamp = time
    time = time.strftime(f)

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
    f = '%Y-%m-%d %H:%M:%S'
    time = datetime.datetime.now()
    if session:
        session.Timestamp = time
    time = time.strftime(f)

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

    ses = new Session(ip=session[0],ts=session[1],resp=session[2],p21=session[3],p22=session[4],p25=session[5],p80=session[6],p139=session[7])
    return ses
