import time, uuid, sys
import socket

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

def httpResponse(server, StatusCode="200 OK", filename='generic.header', body=None):
    # Construct the time strings for the response
    curr_time = time.gmtime()
    last_modified = time.gmtime()
    Date = time.strftime('%a, %d %b %Y %H:%M:%S GMT', curr_time)
    LastModified = time.strftime('%a, %d %b %Y %H:%M:%S GMT', last_modified)

    # Calculate a random guid for the ETag
    ETag = uuid.uuid4().hex[:10]

    # Fetch the body and set the content length
    if (body == None):
        file = open("body.html", "r")
        Body = file.read()
        file.close()
    else:
        Body = body

    ContentLength = len(Body)

    file = open(filename, "r")
    ###file = open("generic.header", "r")
    response =  file.read()
    file.close()
    response = response.replace("#statuscode", StatusCode)
    response = response.replace("#server", server['Server'])
    response = response.replace("#options", server['Options'])
    response = response.replace("#date", Date)
    response = response.replace("#lastmodified", LastModified)
    response = response.replace("#etag", ETag)
    response = response.replace("#contentlength", "%d" % ContentLength)
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

def __main__():
    server = selectServer()
    print('Chose HTTP server %s' % server['Name'])
    listener = createListenerSocket("130.126.143.59", 80)
    while 1 == 1:
        (s, details) = listener.accept()
        print("Got a connection!")

        request = getMessage(s)
        if request != None:
            print(request)
            # Chain of messages to support
            if (request.startswith('GET')):
                response = httpResponse(server, filename=server['GET']['Filename'], StatusCode="200 OK")
                # Determine what flags to use when sending the response based on the FIN settings
                flags = 0
                ###if server['GET']['FIN_w_response']:
                ###    flags = 0
                s.send(response, flags)
            elif (request.startswith('OPTIONS') and 'RTSP' in request):
                response = httpResponse(server, filename=server['OPTIONS_RTSP']['Filename'], body='')
                s.send(response)
            elif (request.startswith('OPTIONS') and 'HTTP' in request):
                response = httpResponse(server, filename=server['OPTIONS_HTTP']['Filename'], body='')
                s.send(response)
        s.close()

__main__()