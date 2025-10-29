class Tcp:
    def extract_ip_addresses(addrs):
        addrs = addrs.decode("utf-8")
        ip_parts = addrs.split(" ")
        src_ip = b""
        dest_ip = b""
        src_ip_array = ip_parts[0].split(".")
        src_ip_array = list(map(int, src_ip_array))
        dest_ip_array = ip_parts[1].split(".")
        dest_ip_array =  list(map(int, dest_ip_array))
        for i in range(0, 4):
            src_ip += int.to_bytes(src_ip_array[i])
            dest_ip += int.to_bytes(dest_ip_array[i])
        return (dest_ip, src_ip)
    
    def build_header(addrs, length):
        header = b""
        dest_addr, src_addr = Tcp.extract_ip_addresses(addrs)
        header += src_addr + dest_addr + b'\x00' + b'\x06' + int.to_bytes(length)
        return header

    def checksum(header, tcp_data):
        data = header + tcp_data
        
        total = 0

        for each in word:
            total += each
            total = (total & 0xffff) + (total >> 16)
        return (~total) & 0xffff

    def verify_tcp(tcp_data, addrs):
        tcp_length = len(tcp_data)
        cksum = int.from_bytes(data[16:18], "big")
        tcp_zero_cksum = data[:16] + b'\x00\x00' + data[18:]
        header = Tcp.build_header(addrs, tcp_length)

        if len(tcp_zero_cksum) % 2 == 1:
            tcp_zero_cksum += b'\x00'

        tcp_data = header + tcp_zero_cksum
        offset = 0
        while offset < len(tcp_data):
            word = int.from_bytes(tcp_data[offset:offset+2], "big")
            offset += 2



        calc_sum = checksum()
        if calc_sum == cksum:
            return "PASS"
        else:
            return "FAIL"

for i in range(0, 10):
    with open(f"tcp_data/tcp_data_{i}.dat", "rb") as data:
        with open(f"tcp_data/tcp_addrs_{i}.txt", "rb") as addrs:
            tcp_data = data.read()
            addrs_data = addrs.read()
            Tcp.verify_tcp(tcp_data, addrs_data)

