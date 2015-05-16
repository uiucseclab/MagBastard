import MySQLdb
import datetime

timeout = 300 # seconds
timestampFormatString = '%Y-%m-%d %H:%M:%S.%f'

def checkResponse(response):
    if response == None:
        return None
    return response.upper() if response.upper() in ('ACCEPT', 'REJECT') else None

class Session:
    def __init__(self, ip='', ts=datetime.datetime.now(), ftp=-1,ssh=-1,smtp=-1,http=-1,samba=-1,ftpResponse=None,sshResponse=None,smtpResponse=None,httpResponse=None,sambaResponse=None):
        self.IP = ip
        self.Timestamp = ts
        self.Ports = {}
        self.Responses = {}
        if ftp != -1:
            self.Ports['ftp'] = ftp
            self.Responses['ftp'] = checkResponse(ftpResponse)
        if ssh != -1:
            self.Ports['ssh'] = ssh
            self.Responses['ssh'] = checkResponse(sshResponse)
        if smtp != -1:
            self.Ports['smtp'] = smtp
            self.Responses['smtp'] = checkResponse(smtpResponse)
        if http != -1:
            self.Ports['http'] = http
            self.Responses['http'] = checkResponse(httpResponse)
        if samba != -1:
            self.Ports['samba'] = samba
            self.Responses['samba'] = checkResponse(sambaResponse)
        

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

def updateSession(session):
    if not session or not session.IP:
        return

    ip = session.IP
    p21 = session.Ports['ftp'] if (session and 'ftp' in session.Ports) else -1
    p21R = session.Responses['ftp'] if (session and 'ftp' in session.Responses) else ''
    p22 = session.Ports['ssh'] if (session and 'ssh' in session.Ports) else -1
    p22R = session.Responses['ssh'] if (session and 'ssh' in session.Responses) else ''
    p25 = session.Ports['smtp'] if (session and 'smtp' in session.Ports) else -1
    p25R = session.Responses['smtp'] if (session and 'smtp' in session.Responses) else ''
    p80 = session.Ports['http'] if (session and 'http' in session.Ports) else -1
    p80R = session.Responses['http'] if (session and 'http' in session.Responses) else ''
    p139 = session.Ports['samba'] if (session and 'samba' in session.Ports) else -1
    p139R = session.Responses['samba'] if (session and 'samba' in session.Responses) else ''
    
    p21R = '' if p21R == None else p21R
    p22R = '' if p22R == None else p22R
    p25R = '' if p25R == None else p25R
    p80R = '' if p80R == None else p80R
    p139R = '' if p139R == None else p139R

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

    query = "SELECT * FROM SessionData WHERE IP='%s'" % (ip)

    cur.execute(query)
    if cur.fetchone():
        query = "UPDATE SessionData SET Timestamp='%s', FTP=%d, SSH=%d, SMTP=%d, HTTP=%d, SAMBA=%d, FTPResponse = '%s', SSHResponse = '%s', SMTPResponse = '%s', HTTPResponse = '%s', SAMBAResponse = '%s' WHERE IP='%s'" % (time, p21,p22,p25,p80,p139,p21R,p22R,p25R,p80R,p139R, ip)
#        print(query)
        cur.execute(query)
        response = cur.fetchone()
#        if response:
#            print(response)
    else:
        #inserting the values into the table
        query = "INSERT INTO SessionData (IP, Timestamp, FTP, SSH, SMTP, HTTP, SAMBA, FTPResponse, SSHResponse, SMTPResponse, HTTPResponse, SAMBAResponse) VALUES ('%s', '%s', %d, %d, %d, %d, %d, '%s', '%s', '%s', '%s', '%s')" % (ip, time, p21,p22,p25,p80,p139,p21R,p22R,p25R,p80R,p139R)
#        print(query)
        cur.execute(query)
        response = cur.fetchone()
#        if response:
#            print(response)

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
#    if response:
#        print(response)

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

    timestamp = datetime.datetime.strptime(session[1], timestampFormatString)
    elapsed = datetime.datetime.now() - timestamp

    if(elapsed.seconds > timeout):
        #return None
	return "timeout"

    ses = Session(ip=session[0],ts=session[1],ftp=int(session[2]),ftpResponse=session[3],ssh=int(session[4]),sshResponse=session[5],smtp=int(session[6]),smtpResponse=session[7],http=int(session[8]),httpResponse=session[9],samba=int(session[10]),sambaResponse=session[11])
#    print ('Ports: %s' % ses.Ports)
#    print ('Responses: %s' % ses.Responses)
    return ses
