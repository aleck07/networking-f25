# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select

def run_server(port):
    read_set = set()
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("localhost", port))
    s.listen()
    read_set.add(s)
    while True:
        read_sockets, _, _ = select.select(read_set, [], [])
        for read_socket in read_sockets:
            if read_socket is s:
                new_conn = read_socket.accept()
                new_socket = new_conn[0]
                read_set.add(new_socket)
            else:
                data = read_socket.recv(1024)
                if not data:
                    read_set.remove(read_socket)
                    read_socket.close()
                else:
                    print(data.decode().strip())

#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
