class Tcp:
    def extract_ip_addresses(addrs):
        addrs = addrs.decode("utf-8").strip()
        ip_parts = addrs.split(" ")
        src_ip = b""
        dest_ip = b""
        src_ip_array = ip_parts[0].split(".")
        src_ip_array = list(map(int, src_ip_array))
        dest_ip_array = ip_parts[1].split(".")
        dest_ip_array = list(map(int, dest_ip_array))
        for i in range(0, 4):
            src_ip += int.to_bytes(src_ip_array[i])
            dest_ip += int.to_bytes(dest_ip_array[i])
        return (src_ip, dest_ip)
    
    def build_header(addrs, length):
        header = b""
        src_addr, dest_addr = Tcp.extract_ip_addresses(addrs)
        header += src_addr + dest_addr + b'\x00' + b'\x06' + int.to_bytes(length, 2, 'big')
        return header

    def checksum(header, tcp_data):
        data = header + tcp_data
        
        total = 0
        offset = 0
        
        while offset < len(data):
            word = int.from_bytes(data[offset:offset+2], "big")
            total += word
            total = (total & 0xffff) + (total >> 16)  # Carry around
            offset += 2
            
        return (~total) & 0xffff  # One's complement

    def verify_tcp(tcp_data, addrs):
        tcp_length = len(tcp_data)
        cksum = int.from_bytes(tcp_data[16:18], "big")
        tcp_zero_cksum = tcp_data[:16] + b'\x00\x00' + tcp_data[18:]
        header = Tcp.build_header(addrs, tcp_length)

        if len(tcp_zero_cksum) % 2 == 1:
            tcp_zero_cksum += b'\x00'

        calc_sum = Tcp.checksum(header, tcp_zero_cksum)

        if calc_sum == cksum:
            return "PASS"
        else:
            return "FAIL"

for i in range(0, 10):
    with open(f"tcp_data/tcp_data_{i}.dat", "rb") as data:
        with open(f"tcp_data/tcp_addrs_{i}.txt", "rb") as addrs:
            tcp_data = data.read()
            addrs_data = addrs.read()
            result = Tcp.verify_tcp(tcp_data, addrs_data)
            print(result)

