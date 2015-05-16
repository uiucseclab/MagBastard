import socket
import datetime
from logging import logger
from ConfigParser import ConfigParser
import plat_dict as plat
import os
from Inetsim import gen_conf_linux
###import sys
###
###if len(sys.argv) > 1:
###    def randint(a, b):
###        return int(sys.argv[1])
###else:
from random import randint

config = ConfigParser()
config.read("magbastard.cfg")
timeout = 300 # seconds

sendRate = int(config.get("default", "sendRate"))
listenAddress = config.get("default", "listenAddress")

serviceMappings = {
    int(config.get("default", "FTPPort")): 'ftp',
    int(config.get("default", "SSHPort")): 'ssh',
    int(config.get("default", "SMTPPort")): 'smtp',
    int(config.get("default", "HTTPPort")): 'http',
    int(config.get("default", "NetBIOSPort")): 'samba',
    int(config.get("default", "HTTPSPort")) : 'https',
    int(config.get("default", "POP3Port")) : 'pop3'
}

def selectServer(configFilename="servers.config", index=None):
    # Read list of supported servers from file
    file = open(configFilename, "r")
    servers = eval(file.read())
    file.close()

    # Choose the server version
    if index == None:
        index = randint(0, len(servers) - 1)
    return (servers[index], index)

def createListenerSocket(host, port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind((host, port))
    listener.listen(10)
    return listener

def getMessage(skt):
    skt.setblocking(1)
    try:
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
    except:
        return None

def sendResponse(skt, msg, flags=0):
    try:
        for i in range(0, len(msg) - sendRate, sendRate):
            skt.send(msg[i:i+sendRate])
        skt.send(msg[len(msg)//sendRate*sendRate:], flags)
    except:
        print("Connection reset by client!")

def startListener(requestHandler, port, configFilename):
    listener = createListenerSocket(listenAddress, port)
    s = None
    try:
        while True:
            (s, details) = listener.accept()
            details = details + (listenAddress,) + (port,)
            print("Got a connection from %s:%d! to %s:%d" % details)
            
            # Check if we have an existing session for this ip address
	    # if this session has been running for > 5min, 
	    #	logger assumes it to be a non-existing session => now logger returns timeout
	    #	(./logging/logger.py)
            #Session = logger.retrieveSession(details[0])
	    if plat.ip_info.has_key(details[0]):
		elapsed = datetime.datetime.now() - plat.ip_info[details[0]][1]
		if elapsed.seconds > timeout:
			session = "timeout"
		else:
			session = logger.retrieveSession(details[0]) #plat.ip_info[details[0]][0]
	    else:
		session = None
            serviceName = serviceMappings[port]
            if session == None:
                index = None
		plat_id = assignServer(details[0])
                session = logger.Session(details[0])
	    elif session == "timeout":
		index = None
		# check if inetsim assigned to this session has other valid sessions
		# if no other session, stop this specific inetsim service 
		# and restart with a new config file
		print plat.ip_info
		plat_id = plat.ip_info[details[0]][0]
		if plat.config_info.has_key(plat_id):
		    plat.config_info[plat_id].remove(details[0])
		    for ipAddr in plat.config_info[plat_id]:
			if logger.retrieveSession(ipAddr) == "timeout":
			    # remove that entry from dict
			    plat.config_info[plat_id].remove(ipAddr)
			    del plat.ip_info[ipAddr]
		    if len(plat.config_info[plat_id]) <= 0:
			del plat.config_info[plat_id]
			pid = str(plat_id)+".pid"
			conf_file = str(plat_id)+".conf"
			os.system("sudo /home/ubuntu/MagBastard/inetsim-daemon stop /var/run/"+pid+" /home/ubuntu/MagBastard/"+conf_file)

		# assign a new inetsim for this session and make any updates necessary
		plat_id = assignServer(details[0])
		session = logger.Session(details[0])
		
            else:
		plat_id = plat.ip_info[details[0]][0]
                index = session.Ports[serviceName] if serviceName in session.Ports else None
            oldIndex = index
            #server, index = selectServer(configFilename=configFilename, index=index)
            # IMPLEMENT ME!! with the new function assignServer, need update on calling selectServer
	    # 		     maybe plat_id can replace server or actually it can replace index.
            responseType = "ACCEPT" if randint(0, 1000) >= 0 else "REJECT"
            if serviceName in session.Responses and session.Responses[serviceName] != None:
#                print("Before: %s; After: %s" % (responseType, session.Responses[serviceName]))
                responseType = session.Responses[serviceName]
                
            # If we didn't have a version string before, add it now
            session.Ports[serviceName] = plat_id #index
            session.Responses[serviceName] = responseType
#            print("Updating to:\n    Ports: %s\n    Responses: %s\n" % (session.Ports, session.Responses))
            logger.updateSession(session)
            
            print("Chose conf_id %d" % plat_id)
            
            print("Chose to %s the connection." % responseType)
            if responseType.upper() == "ACCEPT":
                requestHandler(s, None, details, plat_id)
            else:
                s.close()
    except (KeyboardInterrupt, SystemExit):
        listener.close()
        if s != None:
            s.close()
        print("Exiting...")

def assignServer(srcIP):
    # determine which inetSim to start
    if len(plat.config_info) >= plat.max_config:
        # choose among existing
        plat_id = -1
        while(plat.config_info.has_key(plat_id)): plat_id = randint(1, plat.max_config)
    else:
	# generate a new config and start another inetsim

	while True:
	    plat_id = randint(1, plat.max_config)
	    if(not plat.config_info.has_key(plat_id)): break
	pid = str(plat_id)+".pid"
	conf_file = str(plat_id)+".conf"
	gen_conf_linux.interface(plat_id*1000, conf_file)

	os.system("sudo /home/ubuntu/MagBastard/inetsim-daemon start /var/run/"+pid+" /home/ubuntu/MagBastard/"+conf_file)
    # update the dictionaries that manage the platform assignments
    if plat.config_info.has_key(plat_id): 
	if srcIP not in plat.config_info[plat_id]: plat.config_info[plat_id].append(srcIP)
	else: print "Should not happen"
    else: plat.config_info.update({plat_id : [srcIP]})
    if plat.ip_info.has_key(srcIP): print "Should not happen"
    else: plat.ip_info.update({srcIP : [plat_id, datetime.datetime.now()]})

    return plat_id
