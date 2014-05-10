from resources import ServiceListener
from ConfigParser import ConfigParser
import socket
import threading

config = ConfigParser()
config.read("magbastard.cfg")

kippoaddr = config.get("kippo", "kippoaddr")
kippoport = int(config.get("kippo", "kippoport"))
kippoVerStrFile = config.get("default", "kippoVerStrFile")

def sshHandler(s, server, details):
    # Provide kippo with the version string to use
    f = open(kippoVerStrFile, "w")
    f.write(server["Version"])
    f.close()

    # Connect to Kippo; forward traffic
    kippo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    kippo.connect((kippoaddr, kippoport))
    kippostr = kippo.recv(65535)
    print("From kippo: '%s', %d %d" % (kippostr, ord(kippostr[-2]), ord(kippostr[-1])))

    # Send selected version string as response
    try:
        s.send(server["Version"] + "\r\n")
        ###skt.send(kippostr)

        def sendTo():
            data = 'blah'
            while data != None and data != '':
                data = s.recv(65535)
                ###print ("--->: %s..." % data[:70])
                ###if (len(data) > 2):
                ###    print ('Data ended with %d %d.' % (ord(data[-2]), ord(data[-1])))
                kippo.send(data)
        
        def sendFrom():
            data = 'blah'
            while data != None and data != '':
                data = kippo.recv(65535)
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
