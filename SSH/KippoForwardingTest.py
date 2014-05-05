import socket

ipaddr = 'localhost'
port = 8080
kippoaddr = 'localhost'
kippoport = 2222

# Bind to port 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ipaddr, port))
s.listen(10)

# Listen for connection
(skt, info) = s.accept()
print("Connection established by host %s!" % str(info))

# Connect to Kippo; forward traffic
kippo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
kippo.connect((kippoaddr, kippoport))
print("From kippo: %s" % kippo.recv(65535))

# Send garbage string as response
isOpen = True
s.send("asdlkfjslkdjflskdf")

while isOpen:
    kippo.send(s.recv(65535))
    s.send(kippo.recv(65535))

