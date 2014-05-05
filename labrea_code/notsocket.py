import socket

HOST = '127.0.0.1'
PORT = 23

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

conn, addr = s.accept()

print 'Connection address:', addr
while 1:
	data = conn.recv(20)
	if not data: break
	print "received data:", data
	conn.send(data)
conn.close()
