import time, uuid, sys, re
import socket
import urlparse

# Constants
sendRate = 1000
listenAddress = "localhost"

if len(sys.argv) > 1:
    def randint(a, b):
        return int(sys.argv[1])
else:
    from random import randint

def selectServer():
    # Read list of supported servers from file
    file = open("servers.config", "r")
    servers = eval(file.read())
    file.close()

    # Choose the server version
    return servers[randint(0, len(servers) - 1)]

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
        skt.send(msg)
    except:
        print 'Connection reset'

def __main__():
    server = selectServer()
    print("Chose NetBIOS server %s" % server["Name"])
    listener = createListenerSocket(listenAddress, 139)
    while 1 == 1:
        (s, details) = listener.accept()
        print("Got a connection!")

        request = getMessage(s)
        if request != None and request == '\0\0\0\xa4\xff\x53\x4d\x42\x72\0\0\0\0\x08\x01\x40\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x40\x06\0\0\x01\0\0\x81\0\x02PC NETWORK PROGRAM 1.0\0\x02MICROSOFT NETWORKS 1.03\0\x02MICROSOFT NETWORKS 3.0\0\x02LANMAN1.0\0\x02LM1.2X002\0\x02Samba\0\x02NT LANMAN 1.0\0\x02NT LM 0.12\0':
#        if request != None:
            print(request)
            response = server["Response"]
            sendResponse(s, response)
        s.close()

__main__()
