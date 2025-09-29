import socket
s = socket.socket()
server = ("starwarstel.net", 23)
s.connect(server)
while True:
    data = s.recv(2048)
    str = data.decode("utf-8", errors="ignore")
    print(str, end="")