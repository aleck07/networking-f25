import socket
# Create a socket
s = socket.socket()

# Connect the socket to a server
server = ("time.nist.gov", 13)
s.connect(server)

# Receive data
data = s.recv(256)
print(data.decode())

# Close the connection
s.close()