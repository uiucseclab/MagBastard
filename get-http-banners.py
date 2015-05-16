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

print(" \n \n ***** HTTP Banner Grabbing ***** \n")
#host2 = raw_input("Enter the full URL starts with HTTP or HTTPS \n Enter Url Here => :")
f=open('alexa-top-10000-global.txt','r')
for line in f:
	print line
	req = urllib2.Request("http://" + line, headers={'User-Agent' : 'Mozilla/5.0'})
	try:
		c = urllib2.urlopen(req, None, 20)
		print c.info()
		print c.getcode()
	except urllib2.HTTPError, e:
		print e.fp.read()
	except httplib.BadStatusLine:
        	pass
	except urllib2.URLError:
		pass
	except socket.error:
		pass
	
