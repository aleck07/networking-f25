# This code is to create a simple server.
import socket
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("localhost", 3096))
s.listen()
while True:
    client_socket, client_addr = s.accept()
    print(client_addr)
    client_message = client_socket.recv(256).decode()
    print(client_message)
    client_socket.close()