from resources import ServiceListener
from logging import logger
from ConfigParser import ConfigParser
import socket

config = ConfigParser()
config.read("magbastard.cfg")
inetaddr = config.get("inetsim", "inetaddr")
inetFTPport = int(config.get("inetsim", "inetFTPport"))

def ftpHandler(s, server, details, plat_id):
    request = ServiceListener.getMessage(s)
    logger.updateTimestamp(details[0])
    if request != None:
        logger.logEvent(details[2], details[3], details[0], details[1], request)
        print(request)
	honeypot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	honeypot.connect((inetaddr, inetFTPport + plat_id * 1000))
	# Forward the request to inetsim
	honeypot.send(request)
	#data = 'blah'
	#while data != Nont and data != '':
	
	# Forward the response from inetsim to client
	data = honeypot.recv(65535)
	ServiceListener.sendResponse(s, data)
	logger.logEvent(details[2], details[3], details[0], details[1], data)
	'''
        properRequest = (request.find("\r\n") != -1)
        if properRequest:
            response = server["Version"]
            ServiceListener.sendResponse(s, response)
            logger.logEvent(details[2], details[3], details[0], details[1], response)
	'''
	
    s.close()
