from resources import ServiceListener
from logging import logger

def smtpHandler(s, server, details):
    logger.updateTimestamp(details[0])
    response = server["Version"]
    ServiceListener.sendResponse(s, response)
    logger.logEvent(details[2], details[3], details[0], details[1], response)     
    s.close()
