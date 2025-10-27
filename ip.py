import time
import random

def ip_to_four_byte(ip):
    ip = ip.strip()
    parts = ip.split('.')

    four_byte = 0
    for i in parts:
        four_byte = (four_byte << 8) + int(i)
    
    return four_byte

def four_byte_to_ip(four_byte):
    four_byte = int(four_byte)
    parts = []
    for shift in (24, 16, 8, 0):
        parts.append(str((four_byte >> shift) & 0xFF))

    return '.'.join(parts)


ip = ["192.168.1.2", "10.20.30.40", "127.0.0.1"]
decimal = [3325256824, 3405803976, 3221225987]

start_time = time.time()
for i in range(1, 100000000):
    decimal.append(random.getrandbits(32))
stop_time = time.time()
print(f"Generating random 32bit numbers took: {stop_time-start_time}")

start_time = time.time()
for addr in ip:
    print(ip_to_four_byte(addr))
stop_time = time.time()
print(f"Time taken for IP-Decimal: {stop_time-start_time}")   

start_time = time.time()
for value in decimal:
    four_byte_to_ip
stop_time = time.time()
print(f"Time taken for Decimal-IP: {stop_time-start_time}")
