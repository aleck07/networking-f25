import socket
# Create a socket
s = socket.socket()

# Connect the socket to a server
server = ("localhost", 3096)
s.connect(server)

userInput = input("Type your message: ")

# Send data

s.sendall(userInput.encode())

# Receive data
data = s.recv(256)
print(data.decode())

# Close the connection
s.close()