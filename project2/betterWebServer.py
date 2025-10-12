import socket
import sys
import os

def getMime(file_name):
    extension = os.path.splittext(file_name)[1]
    if extension == ".txt":
        return "text/plain"
    elif extension == ".html":
        return "text/html"
    else:
        return "text/html"

def main():
    # Check system args
    if len(sys.argv) < 2:
        port = 28333
    else:
        port = int(sys.argv[1])

    s = socket.socket()
    request = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 6\r\nConnection: close\r\n\r\nHello!"
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print(port)
    s.bind(("localhost", port))
    s.listen()
    while True:
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
        file_name = full_path.split("/")[-1]
        print(file_name)
        new_socket.sendall(request.encode("ISO-8859-1"))
        new_socket.close()

if __name__ == "__main__":
    main()