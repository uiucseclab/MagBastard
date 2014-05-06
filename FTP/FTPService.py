from resources import ServiceListener

def ftpHandler(s, server):
    request = ServiceListener.getMessage(s)
    if request != None:
        print(request)
        properRequest = (request.find("\r\n") != -1)
        if properRequest:
            response = server["Version"]
            ServiceListener.sendResponse(s, response)

    s.close()
