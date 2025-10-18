import socket
import time

def main():
    s = socket.socket()
    server = ("time.nist.gov", 37)
    s.connect(server)
    data = s.recv(4)
    data = int.from_bytes(data, "big")
    print(f"Nist time   : {data}")
    print(f"System time : {system_seconds_since_1900()}")

def system_seconds_since_1900():
    """
    The time server returns the number of seconds since 1900, but Unix
    systems return the number of seconds since 1970. This function
    computes the number of seconds since 1900 on the system.
    """

    # Number of seconds between 1900-01-01 and 1970-01-01
    seconds_delta = 2208988800

    seconds_since_unix_epoch = int(time.time())
    seconds_since_1900_epoch = seconds_since_unix_epoch + seconds_delta

    return seconds_since_1900_epoch

if __name__ == "__main__":
    main()