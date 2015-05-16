from resources import ServiceListener
from ConfigParser import ConfigParser
import socket
import threading
import random

config = ConfigParser()
config.read("magbastard.cfg")

kippoaddr = config.get("kippo", "kippoaddr")
#inetaddr = config.get("inetsim", "inetaddr")
kippoport = int(config.get("kippo", "kippoport"))
#inetSSHport = int(config.get("inetsim", "inetSSHport"))

kippoVerStrFile = config.get("default", "kippoVerStrFile")

# Rate of SSH requests forwared to Kippo [0, 1.0]
kippoRate = config.get("default", "kippoRate") 


def sshHandler(s, server, details, plat_id):
    # Provide kippo with the version string to use
    f = open(kippoVerStrFile, "w")
    f.write(server["Version"])
    f.close()

    honeypot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #x = random.random() # generate a random integer
    #if x < kippoRate:
	# Connect to Kippo
    honeypot.connect((kippoaddr, kippoport))
    honeypotstr = honeypot.recv(65535)
    print("From kippo: '%s', %d %d" % (honeypotstr, ord(honeypotstr[-2]), ord(honeypotstr[-1])))
    #else:
	# Connect to Inetsim
    	#honeypot.connect((inetaddr, inetSSHport))

    # Forward traffic
    # Send selected version string as response
    try:
        s.send(server["Version"] + "\r\n")
        ###skt.send(kippostr)

        def sendTo():
            data = 'blah'
            while data != None and data != '':
                data = s.recv(65535)
		logger.updateTimestamp(details[0])
		logger.logEvent(details[2], details[3], details[0], details[1], data)  # Logs the ssh request to the DB
                ###print ("--->: %s..." % data[:70])
                ###if (len(data) > 2):
                ###    print ('Data ended with %d %d.' % (ord(data[-2]), ord(data[-1])))
                honeypot.send(data)
        
        def sendFrom():
            data = 'blah'
            while data != None and data != '':
                data = honeypot.recv(65535)
		logger.updateTimestamp(details[0])
		logger.logEvent(details[2], details[3], details[0], details[1], data) # Log the ssh response from Kippo to the DB
                ###if (len(data) > 2):
                ###    print ('Data ended with %d %d.' % (ord(data[-2]), ord(data[-1])))
                ###print ("<---: %s..." % data[:70])
                s.send(data)

        sender = threading.Thread(target=sendTo)
        sender.start()
        th = threading.Thread(target=sendFrom)
        th.daemon = True
        th.start()
        
        sender.join()
    except:
        print("Client closed the connection!")
