#!/usr/bin/env/python3.1
#mls577
#haxme, #suidrewt

import sys, socket #module imports
if(len(sys.argv) == 3): #argument length check

    host = sys.argv[1] #host
    port = sys.argv[2] #port

    #create socket
    s = socket.socket()

    try:
        connect = s.connect((host, int(port))) #connect to the host
        banner = s.recv(1024) #recieve the banner
        print(banner) #print the output
        s.close() #close socket
		
    except socket.error:
        s.close() #close socket
        print("socket error")

else:
        print("usage: program.py <host> <port>")

