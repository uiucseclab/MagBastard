import socket
from logging import logger

###import sys
###
###if len(sys.argv) > 1:
###    def randint(a, b):
###        return int(sys.argv[1])
###else:
from random import randint

# Constants
sendRate = 1000
listenAddress = "localhost"

serviceMappings = {
    10021: 'ftp',
    10022: 'ssh',
    10025: 'smtp',
    10080: 'http',
    10139: 'samba'
}

def selectServer(configFilename="servers.config", index=None):
    # Read list of supported servers from file
    file = open(configFilename, "r")
    servers = eval(file.read())
    file.close()

    # Choose the server version
    if index == None:
        index = randint(0, len(servers) - 1)
    return servers[index]

def createListenerSocket(host, port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind((host, port))
    listener.listen(10)
    return listener

def getMessage(skt):
    skt.setblocking(1)
    try:
        message = skt.recv(1)
        if (len(message) < 1):
            return None
        skt.setblocking(0)
        while True:
            try:
                message += skt.recv(100)
            except socket.error:
                break;
        skt.setblocking(1)
        return message
    except:
        return None

def sendResponse(skt, msg, flags=0):
    try:
        for i in range(0, len(msg) - sendRate, sendRate):
            skt.send(msg[i:i+sendRate])
        skt.send(msg[len(msg)//sendRate*sendRate:], flags)
    except:
        print("Connection reset by client!")

def startListener(requestHandler, port, configFilename):
    listener = createListenerSocket(listenAddress, port)
    s = None
    try:
        while True:
            (s, details) = listener.accept()
            details = details + (listenAddress,) + (port,)
            print("Got a connection from %s:%d! to %s:%d" % details)
            
            # Check if we have an existing session
            session = logger.retrieveSession(details[0])
            serviceName = serviceMappings[port]
            if session == None:
                index = None
                session = logger.Session(listenAddress)
            else:
                if serviceName in session.Ports:
                    index = session.Ports[serviceName]
            server = selectServer(configFilename=configFilename, index=index)
            
            responseType = "ACCEPT" if randint(0, 1000) >= 500 else "REJECT"
            if serviceName in session.Responses and session.Responses[serviceName] != None:
                responseType = session.Responses[serviceName]
                
            # If we didn't have a version string before, add it now
            if index == None:
                session.Ports[serviceMappings[port]] = server["Version"]
                session.Responses[serviceMappings[port]] = responseType
                logger.updateSession(session)
            
            print("Chose server %s" % server["Name"])
            
            print("Chose to %s the connection." % responseType)
            if responseType.upper() == "ACCEPT":
                requestHandler(s, server, details)
            else:
                s.close()
    except (KeyboardInterrupt, SystemExit):
        listener.close()
        if s != None:
            s.close()
        print("Exiting...")

