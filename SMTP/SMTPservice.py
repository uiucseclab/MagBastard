from resources import ServiceListener

def smtpHandler(s, server):
	response = server["Version"]
	ServiceListener.sendResponse(s, response)
	s.close()
