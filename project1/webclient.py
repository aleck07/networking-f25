import socket
import sys

s = socket.socket()
if len(sys.argv) < 2:
    hostname = "google.com"
    port = 80
elif len(sys.argv) == 2:
    hostname = sys.argv[1]
    port = 80
else:
    hostname = sys.argv[1]
    port = int(sys.argv[2])

server = (hostname, port)
print(server)
request = f"GET / HTTP/1.1\r\nHost: {hostname}\r\nConnection: close\r\n\r\n"

s.connect(server)
s.sendall(request.encode("ISO-8859-1"))
data = b""
while True:
    d = s.recv(4096)
    if len(d) != 0:
        data += d
    else:
        break

print(data.decode("ISO-8859-1"))
s.close()