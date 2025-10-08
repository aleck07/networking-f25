def split_ip_and_mask(ip, mask):
    ip_portion = []
    host_portion = []
    for i in range(4):
        ip_portion.append(ip[i] & mask[i])
        host_portion.append(ip[i] & (255 - mask[i]))
    return (ip_portion, host_portion)

samples = [
    ([192,168,17,2], [255,0,0,0]),
    ([192,168,17,2], [255,255,0,0]),
    ([192,168,17,2], [255,255,255,0]),
    ([192,168,17,2], [255,192,0,0]),
    ([192,168,17,2], [255,255,248,0]),
]

for ip, mask in samples:
    print(f"{(ip, mask)} : {split_ip_and_mask(ip, mask)}")
