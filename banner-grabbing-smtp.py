import socket
import urllib2           

import socket
import urllib2

# FTP Fingerprinting
host1 =  str(raw_input("Enter the IP adress of the domain:"))
print(" \n \n ***** SMTP Banner Grabbing ***** \n")
socket.setdefaulttimeout(33)
con = socket.socket()
con.connect((host1,25))
result = con.recv(33333)
print result


#HTTP FINGERPRINTING SCRIPT
#print(" \n \n ***** HTTP Banner Grabbing ***** \n")
#host2 = raw_input("Enter the full URL starts with HTTP or HTTPS \n Enter Url Here => :")
#c = urllib2.urlopen(host2)
#print c.info()
#print c.getcode()
