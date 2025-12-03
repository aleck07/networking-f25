import sys
import socket
import select
import json

def pack_message(obj):
    """Pack a JSON object into a 2-byte length + JSON payload."""
    payload = json.dumps(obj).encode("utf-8")
    length = len(payload)
    length_bytes = length.to_bytes(2, "big")
    return length_bytes + payload

def extract_packets(buffer):
    """
    Extract complete packets from buffer.
    Returns (list_of_packets, remaining_buffer)
    """
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

def broadcast(sockets, listener, buffers, nicks, obj, exclude=None):
    """Broadcast a message to all connected clients."""
    data = pack_message(obj)
    
    for sock in list(sockets):
        if sock is listener:
            continue
        if exclude and sock is exclude:
            continue
            
        try:
            sock.sendall(data)
        except:
            # Remove disconnected client
            if sock in sockets:
                sockets.remove(sock)
            buffers.pop(sock, None)
            nick = nicks.pop(sock, None)
            try:
                sock.close()
            except:
                pass
            if nick:
                broadcast(sockets, listener, buffers, nicks, {"type": "leave", "nick": nick})

def run_server(port):
    read_set = set()
    buffers = {}
    nicks = {}
    
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("", port))
    s.listen()
    read_set.add(s)
    
    print(f"Chat server listening on port {port}")
    
    while True:
        read_sockets, _, _ = select.select(read_set, [], [])
        
        for read_socket in read_sockets:
            if read_socket is s:
                # New connection
                new_conn = read_socket.accept()
                new_socket = new_conn[0]
                addr = new_conn[1]
                read_set.add(new_socket)
                buffers[new_socket] = b""
                print(f"{addr}: connected")
            else:
                # Data from existing client
                data = read_socket.recv(4096)
                
                if not data:
                    # Client disconnected
                    addr = read_socket.getpeername()
                    print(f"{addr}: disconnected")
                    read_set.remove(read_socket)
                    buffers.pop(read_socket, None)
                    nick = nicks.pop(read_socket, None)
                    read_socket.close()
                    
                    if nick:
                        broadcast(read_set, s, buffers, nicks, {"type": "leave", "nick": nick})
                else:
                    # Process received data
                    buffers[read_socket] += data
                    packets, buffers[read_socket] = extract_packets(buffers[read_socket])
                    
                    for packet in packets:
                        packet_type = packet.get("type")
                        
                        if packet_type == "hello":
                            nick = packet.get("nick", "")
                            if nick:
                                nicks[read_socket] = nick
                                broadcast(read_set, s, buffers, nicks, {"type": "join", "nick": nick})
                        
                        elif packet_type == "chat":
                            if read_socket in nicks:
                                msg = packet.get("message", "")
                                chat_packet = {"type": "chat", "nick": nicks[read_socket], "message": msg}
                                broadcast(read_set, s, buffers, nicks, chat_packet)

def usage():
    print("usage: chat_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))