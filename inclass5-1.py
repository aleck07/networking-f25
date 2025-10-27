# IP address to decimal value
# Decimal value to ip address
# Answers:
# 3232235778
# 169090600
# 2130706433
# 198.51.100.120
# 203.0.113.200
# 192.0.2.3

def ip_to_decimal(ip):
    ip = ip.split(".")
    sum = 0
    for i in range(1, 5):
        sum += int(ip[-i])*(256**(i-1))
    return sum


def decimal_to_ip(decimal):
    remain = []
    for i in range(1, 5):
        remain.append(str(decimal % 256))
        decimal = decimal // 256
    remain.reverse()
    remain = ".".join(remain)
    return remain 



ip = ["192.168.1.2", "10.20.30.40", "127.0.0.1"]
decimal = [3325256824, 3405803976, 3221225987]

for addr in ip:
    print(ip_to_decimal(addr))

for value in decimal:
    print(decimal_to_ip(value))