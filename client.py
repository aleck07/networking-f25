import socket
import json

# Initialize/check user account
with open ("data/account.json", "r") as f:
    userAccount = json.load(f)
if userAccount["username"] == "" or userAccount["hash"] == "":
    userAccount["username"] = input("Enter your username: ")
    userAccount["hash"] = input("Enter your password hash: ")
    with open ("data/account.json", "w") as f:
        json.dump(userAccount, f)


# Create a socket
s = socket.socket()

# Connect the socket to a server
server = ("localhost", 3096)
s.connect(server)

while True:
    # Get user input
    userInput = input("Type your message: ")
    message = f"{userAccount['username']} {userAccount['hash']} {userInput}"

    # Send data
    try:
        message.split(" ")[1]
    except IndexError:
        exit()
    s.sendall(message.encode())

    # Receive data
    # data = s.recv(256)
    # print(data.decode())

# Close the connection
s.close()