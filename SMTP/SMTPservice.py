import time, uuid, sys, re
import socket
import urlparse

# Constants
sendRate = 1000
listenAddress = "172.16.200.240" 

if len(sys.argv) > 1:
    def randint(a, b):
        return int(sys.argv[1])
else:
    from random import randint

def selectServer():
    # Read list of supported servers from file
    file = open("SMTPservers.config", "r")
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
    skt.send(msg)

def __main__():
    server = selectServer()
    print("Chose SMTP server %s" % server["Name"])
    listener = createListenerSocket(listenAddress, 25)
    while 1 == 1:
        (s, details) = listener.accept()
        print("Got a connection!")
	if(server["Name"] == "Postfix"):
		response = server["Response"]
	elif(server["Name"] == "Sendmail"):
		response = server["Response"]
	elif(server["Name"] == "Qmail"):
		response = server["Response"]
        sendResponse(s, response)
        s.close()

__main__()
