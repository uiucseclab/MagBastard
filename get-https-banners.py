import socket
import urllib2           

import socket
import urllib2

# FTP Fingerprinting
#host1 =  str(raw_input("Enter the IP adress of the domain:"))
#print(" \n \n ***** FTP Banner Grabbing ***** \n")
#socket.setdefaulttimeout(33)
#con = socket.socket()
#con.connect((host1,21))
#result = con.recv(33333)
#print result

print(" \n \n ***** HTTP Banner Grabbing ***** \n")
#host2 = raw_input("Enter the full URL starts with HTTP or HTTPS \n Enter Url Here => :")
f=open('alexa-top-10000-global.txt','r')
for line in f:
	print line
	c = urllib2.urlopen("http://" + line)
	print c.info()
	print c.getcode()
