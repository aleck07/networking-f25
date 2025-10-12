import socket
import sys
import os

def getMime(file_name):
    extension = os.path.splitext(file_name)[1]
    if extension == ".txt":
        return "text/plain"
    elif extension == ".html":
        return "text/html"
    else:
        return "text/html"

def fileNotFound():
    return "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: 13\r\nConnection: close\r\n\r\n404 not found"

def isFile(file_name):
    if os.path.exists(file_name):
        return True
    else:
        return False

def readFile(file_name):
    with open(file_name, "rb") as fp:
        data = fp.read()
        return data

def createRequest(file_name):
    data = readFile(file_name).decode()
    mime_type = getMime(file_name)
    content_length = len(data)
    return f"HTTP/1.1 200 OK\r\nContent-Type: {mime_type}\r\nContent-Length: {content_length}\r\nConnection: close\r\n\r\n{data}"

def handleSocket(s):
    new_conn = s.accept()
    new_socket = new_conn[0]
    data = b""
    while True:
        d = new_socket.recv(100)
        data = data + d
        if "\r\n\r\n" in d.decode("ISO-8859-1"):
            break
    data = data.decode("ISO-8859-1")
    # Get full path of request 
    full_path = data.split("HTTP")[0].split("GET")[1]
    file_name = full_path.split("/")[-1].strip()
    request = ""
    if isFile(file_name):
        request = createRequest(file_name)
    else:
        request = fileNotFound()
    new_socket.sendall(request.encode("ISO-8859-1"))
    new_socket.close()

def main():
    # Check system args
    if len(sys.argv) < 2:
        port = 28333
    else:
        port = int(sys.argv[1])

    s = socket.socket()
    request = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 6\r\nConnection: close\r\n\r\nHello!"
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print(f"Port: {port}")
    s.bind(("localhost", port))
    s.listen()
    while True:
        handleSocket(s)

if __name__ == "__main__":
    main()