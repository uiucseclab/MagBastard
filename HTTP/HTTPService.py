import time, uuid, sys, re
import socket
import urlparse

# Constants
sendRate = 1000
listenAddress = "localhost"

if len(sys.argv) > 1:
    def randint(a, b):
        return int(sys.argv[1])
else:
    from random import randint

def selectServer():
    # Read list of supported servers from file
    file = open("servers.config", "r")
    servers = eval(file.read())
    file.close()

    # Choose the server version
    return servers[randint(0, len(servers) - 1)]

def httpResponse(server, StatusCode="200 OK", ContentType="text/html", filename="generic.header", body="no_wai.html"):
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
    response = response.replace("#server", server["Server"])
    response = response.replace("#options", server["Options"])
    response = response.replace("#date", Date)
    response = response.replace("#lastmodified", LastModified)
    response = response.replace("#etag", ETag)
    response = response.replace("#contentlength", "%d" % ContentLength)
    response = response.replace("#contenttype", ContentType)
    response = response + Body
    return response

def createListenerSocket(host, port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind((host, port))
    listener.listen(10)
    return listener


def getMessage(skt):
    skt.setblocking(1)
    message = skt.recv(1)
    if (len(message) < 1):
        return None
    skt.setblocking(0)
    while True:
        try:
            message += skt.recv(100)
        except socket.error:
            break;
    skt.setblocking(1)
    return message

def sendResponse(skt, msg, flags=0):
    for i in range(0, len(msg) - sendRate, sendRate):
        skt.send(msg[i:i+sendRate])
    skt.send(msg[len(msg)//sendRate*sendRate:], flags)

def __main__():
    server = selectServer()
    print("Chose HTTP server %s" % server["Name"])
    listener = createListenerSocket(listenAddress, 80)
    while 1 == 1:
        (s, details) = listener.accept()
        print("Got a connection!")

        request = getMessage(s)
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
                            response = httpResponse(server, filename=server["GET"]["Filename"], body="index.html")
                        elif (path == "/orly_owl.jpg" or path == "orly_owl.jpg"):
                            response = httpResponse(server, filename=server["GET"]["Filename"], body="orly_owl.jpg", ContentType="image/jpeg")
                        elif (path == "/no_wai_owl.jpg" or path == "no_wai_owl.jpg"):
                            response = httpResponse(server, filename=server["GET"]["Filename"], body="no_wai_owl.jpg", ContentType="image/jpeg")
                if response == None:
                    response = httpResponse(server, filename=server["GET"]["Filename"])
                # Determine what flags to use when sending the response based on the FIN settings
                flags = 0
                ###if server["GET"]["FIN_w_response"]:
                ###    flags = 0
                sendResponse(s, response, flags)
            elif (request.startswith("OPTIONS ") and "RTSP" in request and properRequest):
                response = httpResponse(server, filename=server["OPTIONS_RTSP"]["Filename"], body="nobody.html")
                sendResponse(s, response)
            elif (request.startswith("OPTIONS ") and "HTTP" in request and properRequest):
                response = httpResponse(server, filename=server["OPTIONS_HTTP"]["Filename"], body="nobody.html")
                sendResponse(s, response)
        s.close()

__main__()