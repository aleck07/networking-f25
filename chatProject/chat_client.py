from chatui import init_windows, read_command, print_message, end_windows

import sys
import socket
import threading
import json

def usage():
    print("usage: chat_client.py nick host port", file=sys.stderr)

def pack_message(obj):
    payload = json.dumps(obj).encode("utf-8")
    length = len(payload)
    length_bytes = length.to_bytes(2, "big")
    return length_bytes + payload

def extract_packets(buffer):
    packets = []
    offset = 0
    
    while True:
        if len(buffer) - offset < 2:
            break
            
        length = int.from_bytes(buffer[offset:offset+2], "big")
        
        if len(buffer) - offset - 2 < length:
            break
            
        payload_bytes = buffer[offset+2:offset+2+length]
        offset += 2 + length
        
        try:
            packet = json.loads(payload_bytes.decode("utf-8"))
            packets.append(packet)
        except:
            # Skip bad packet
            pass
    
    return packets, buffer[offset:]

def receiver_thread(sock):
    buf = b""
    
    try:
        while True:
            chunk = sock.recv(4096)
            
            if not chunk:
                print_message("*** disconnected from server")
                break
                
            buf += chunk
            packets, buf = extract_packets(buf)
            
            for packet in packets:
                packet_type = packet.get("type")
                
                if packet_type == "join":
                    nick = packet.get("nick", "")
                    print_message(f"*** {nick} has joined the chat")
                    
                elif packet_type == "leave":
                    nick = packet.get("nick", "")
                    print_message(f"*** {nick} has left the chat")
                    
                elif packet_type == "chat":
                    nick = packet.get("nick", "")
                    msg = packet.get("message", "")
                    print_message(f"{nick}: {msg}")
    except:
        pass


def main(argv):
    try:
        nickname = argv[1]
        host = argv[2]
        port = int(argv[3])
    except:
        usage()
        return 1

    s = socket.socket()
    s.connect((host, port))

    # Initialize UI before starting receiver
    init_windows()

    # Start receiver thread
    t = threading.Thread(target=receiver_thread, args=(s,), daemon=True)
    t.start()

    # Send hello packet
    hello_packet = pack_message({"type": "hello", "nick": nickname})
    s.sendall(hello_packet)

    try:
        while True:
            line = read_command(f"{nickname}> ")
            
            if not line:
                continue
                
            if line.startswith("/q"):
                break
                
            # Send chat packet
            chat_packet = pack_message({"type": "chat", "message": line})
            s.sendall(chat_packet)
            
    except KeyboardInterrupt:
        pass
    finally:
        try:
            s.close()
        except:
            pass
        end_windows()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
