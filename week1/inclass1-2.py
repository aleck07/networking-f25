import socket
s = socket.socket()
server = ("flip.engr.oregonstate.edu", 2187)
s.connect(server)
while True:
    data = s.recv(2048)
    str = data.decode("utf-8", errors="ignore")
    print(str, end="")