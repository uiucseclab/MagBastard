def test(dest):
     h1 = http.client.HTTPConnection(dest)
     h1.request('GET', '/')
     time.sleep(1)
     h1 = http.client.HTTPConnection(dest)
     h1.request('OPTIONS', '/')
     time.sleep(1)
     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     s.connect((dest, 80))
     s.send(b'OPTIONS / RTSP/1.0\r\n\r\n')
     s.close()

