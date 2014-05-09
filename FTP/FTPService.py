from resources import ServiceListener
from logging import logger

def ftpHandler(s, server, details):
    request = ServiceListener.getMessage(s)
    logger.updateTimestamp(details[0])
    if request != None:
        logger.logEvent(details[2], details[3], details[0], details[1], request)
        print(request)
        properRequest = (request.find("\r\n") != -1)
        if properRequest:
            response = server["Version"]
            ServiceListener.sendResponse(s, response)
            logger.logEvent(details[2], details[3], details[0], details[1], response)
    s.close()
