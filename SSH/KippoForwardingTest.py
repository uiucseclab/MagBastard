import socket

ipaddr = 'localhost'
port = 8080
kippoaddr = 'localhost'
kippoport = 2222

# Bind to port 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ipaddr, port))
s.listen(10)

# Listen for connection
(skt, info) = s.accept()
print("Connection established by host %s!" % str(info))

# Connect to Kippo; forward traffic
kippo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
kippo.connect((kippoaddr, kippoport))
kippostr = kippo.recv(65535)
val = ''
for c in kippostr:
    val += str(ord(c)) + ' '
print("From kippo: [%s]" % val)

# Send garbage string as response
isOpen = True
skt.send("SSH-2.0-OpenSSH_5.1p1 Debian-5\r\n")
#skt.send(kippostr)

import threading
def sendTo():
    data = 'blah'
    while data != None and data != '':
        data = skt.recv(65535)
        print ("--->: %s..." % data[:70])
	if (len(data) > 2):
            print ('Data ended with %d %d.' % (ord(data[-2]), ord(data[-1])))
        kippo.send(data)

def sendFrom():
    data = 'blah'
    while data != None and data != '':
        data = kippo.recv(65535)
	if (len(data) > 2):
            print ('Data ended with %d %d.' % (ord(data[-2]), ord(data[-1])))
        print ("<---: %s..." % data[:70])
        skt.send(data)

sender = threading.Thread(target=sendTo)
sender.start()
th = threading.Thread(target=sendFrom)
th.daemon = True
th.start()

sender.join()
