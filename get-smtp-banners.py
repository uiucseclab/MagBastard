import socket
import urllib2           
import httplib

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

#host2 = raw_input("Enter the full URL starts with HTTP or HTTPS \n Enter Url Here => :")
f=open('smtp-list.txt','r')
for line in f:
	print line
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
	s.settimeout(10)
	try:
        	s.connect((line.rstrip('\n'), 587))  
        	banner = s.recv(1024)  
      		print line + ':' + banner
	except: 
		pass  
	
