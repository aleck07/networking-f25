# Offset │ Length │ Description
# ───────┼────────┼──────────────────────────────────────────────────
#   0    │    2   │ Total encoded length, including message and value
#   2    │    n   │ The message string encoded as UTF-8
#  2+n   │    4   │ The value encoded as 4-byte 2's complement

def encode_data(message, value):
    message_bytes = message.encode('utf-8')
    message_length = len(message_bytes)
    total_length = 2 + message_length + 4

    encoded = bytearray()
    encoded += total_length.to_bytes(2, byteorder='big')
    encoded += message_bytes
    encoded += value.to_bytes(4, byteorder='big', signed=True)

    return bytes(encoded)

def decode_data(data):
    length = int.from_bytes(data[0:2], byteorder='big')
    value = int.from_bytes(data[-4:], byteorder='big', signed=True)
    message = data[2:-4].decode('utf-8')

    return (message, value)

string = "Hello World!"
encoded_string = encode_data(string, 5293)
decoded_string = decode_data(encoded_string)
print(encoded_string)
print(decoded_string)