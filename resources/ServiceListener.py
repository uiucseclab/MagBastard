import socket
#from logging import logger

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
    for i in range(0, len(msg) - sendRate, sendRate):
        skt.send(msg[i:i+sendRate])
    skt.send(msg[len(msg)//sendRate*sendRate:], flags)

def startListener(requestHandler, port, configFilename):
    listener = createListenerSocket(listenAddress, port)
    s = None
    try:
        while True:
            (s, details) = listener.accept()
            print("Got a connection from %s:%d!" % details)
            
            # Check if we have an existing session
            #session = logger.retrievesession(details[0])
            #if session == None:
            #    index = None:
            #else:
            #    index = session.versions[port]
            server = selectServer(configFilename=configFilename, index=None)#index)
            
            print("Chose server %s" % server["Name"])
            requestHandler(s, server)
    except (KeyboardInterrupt, SystemExit):
        listener.close()
        if s != None:
            s.close()
        print("Exiting...")

