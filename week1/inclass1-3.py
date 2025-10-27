# This code is to create a simple server.
import socket
import json
PORT = 3096
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("localhost", PORT))
s.listen()
print(f"Server is listening on port {PORT}...")
client_socket, client_addr = s.accept()

while True:
    print(client_addr)
    clientData = client_socket.recv(256).decode()
    clientUsername = clientData.split(" ")[0]
    clientHash = clientData.split(" ")[1]
    clientMessage = clientData.lstrip(f"{clientUsername} {clientHash} ")

    # Checks username and hash
    with open ("data/server.json", "r") as f:
        serverAccount = json.load(f)
    if clientUsername != serverAccount["username"] or clientHash != serverAccount["hash"]:
        client_socket.sendall("Invalid username or password hash.".encode())
        client_socket.close()
        continue

    client_socket.sendall(clientMessage.encode())
    print("Message received from " + clientUsername + ": " + clientMessage)
    with open("data/messages.txt", "a") as f:
        f.write(clientUsername + " " + clientMessage + "\n")

