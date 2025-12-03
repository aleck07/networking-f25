from chatui import init_windows, read_command, print_message, end_windows

import sys
import socket
import time
import random

def usage():
    print("usage: select_client.py prefix host port", file=sys.stderr)

def delay_random_time():
    delay_seconds = random.uniform(1, 5)
    time.sleep(delay_seconds)

def main(argv):
    try:
        nickname = argv[1]
        host = argv[2]
        port = int(argv[3])
    except:
        usage()
        return 1

    # Make the client socket and connect
    s = socket.socket()
    s.connect((host, port))

    s.

    # Loop forever sending data at random time intervals
    while True:
        string_to_send = f"{nickname}: "
        string_bytes = string_to_send.encode()
        s.send(string_bytes)

        delay_random_time()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
