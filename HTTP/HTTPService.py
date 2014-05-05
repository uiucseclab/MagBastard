import urlparse
import time, uuid, sys, re
from resources import ServiceListener

def httpResponse(server, StatusCode="200 OK", ContentType="text/html", filename="HTTP/generic.header", body="HTTP/no_wai.html"):
    # Construct the time strings for the response
    curr_time = time.gmtime()
    last_modified = time.gmtime()
    Date = time.strftime("%a, %d %b %Y %H:%M:%S GMT", curr_time)
    LastModified = time.strftime("%a, %d %b %Y %H:%M:%S GMT", last_modified)

    # Calculate a random guid for the ETag
    ETag = uuid.uuid4().hex[:10]

    # Fetch the body and set the content length
    file = open(body, "rb")
    Body = file.read()
    file.close()

    ContentLength = len(Body)

    file = open(filename, "r")
    ###file = open("generic.header", "r")
    response =  file.read()
    file.close()
    response = response.replace("#statuscode", StatusCode)
    response = response.replace("#server", server["Version"])
    response = response.replace("#options", server["Options"])
    response = response.replace("#date", Date)
    response = response.replace("#lastmodified", LastModified)
    response = response.replace("#etag", ETag)
    response = response.replace("#contentlength", "%d" % ContentLength)
    response = response.replace("#contenttype", ContentType)
    response = response + Body
    return response

def httpHandler(s, server):
    request = ServiceListener.getMessage(s)
    if request != None:
        print(request)
        properRequest = (request.find("\r\n\r\n") != -1)
        # Chain of messages to support
        if (request.startswith("GET ") and properRequest):
            URL = request.split("\r\n")[0][3:].strip()
            properRequest = (URL.endswith("HTTP/1.0") or URL.endswith("HTTP/1.1"))
            response = None
            if properRequest:
                URL = urlparse.urlparse(URL[:URL.rfind("HTTP/")].strip())
                properRequest = (URL.params == URL.query == URL.fragment == "")
                path = URL.path.lower()
                if properRequest:
                    if (path == "/index.html" or path == "index.html" or path == "/"):
                        response = httpResponse(server, filename="HTTP/"+server["GET"]["Filename"], body="HTTP/index.html")
                    elif (path == "/orly_owl.jpg" or path == "orly_owl.jpg"):
                        response = httpResponse(server, filename="HTTP/"+server["GET"]["Filename"], body="HTTP/orly_owl.jpg", ContentType="image/jpeg")
                    elif (path == "/no_wai_owl.jpg" or path == "no_wai_owl.jpg"):
                        response = httpResponse(server, filename="HTTP/"+server["GET"]["Filename"], body="HTTP/no_wai_owl.jpg", ContentType="image/jpeg")
            if response == None:
                response = httpResponse(server, filename="HTTP/"+server["GET"]["Filename"])
            # Determine what flags to use when sending the response based on the FIN settings
            flags = 0
            ###if server["GET"]["FIN_w_response"]:
            ###    flags = 0
            ServiceListener.sendResponse(s, response, flags)
        elif (request.startswith("OPTIONS ") and "RTSP" in request and properRequest):
            response = httpResponse(server, filename="HTTP/"+server["OPTIONS_RTSP"]["Filename"], body="HTTP/nobody.html")
            ServiceListener.sendResponse(s, response)
        elif (request.startswith("OPTIONS ") and "HTTP" in request and properRequest):
            response = httpResponse(server, filename="HTTP/"+server["OPTIONS_HTTP"]["Filename"], body="HTTP/nobody.html")
            ServiceListener.sendResponse(s, response)
    s.close()

