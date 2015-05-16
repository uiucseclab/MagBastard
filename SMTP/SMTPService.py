from resources import ServiceListener
from logging import logger
from ConfigParser import ConfigParser
import socket

config = ConfigParser()
config.read("magbastard.cfg")
inetaddr = config.get("inetsim", "inetaddr")
inetSMTPport = int(config.get("inetsim", "inetSMTPport"))


def smtpHandler(s, server, details, plat_id):
    request = ServiceListener.getMessage(s)
    logger.updateTimestamp(details[0])
    print request
    honeypot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    honeypot.connect((inetaddr, inetSMTPport + plat_id * 1000))
    honeypot.send(request)
    response = honeypot.recv(65535)
    '''
    response = server["Version"]
    '''
    ServiceListener.sendResponse(s, response)
    logger.logEvent(details[2], details[3], details[0], details[1], response)     
    s.close()
