import sys
import json
import math  # If you want to use math.inf for infinity

def dijkstras_shortest_path(routers, src_ip, dest_ip):
    """
    This function takes a dictionary representing the network, a source
    IP, and a destination IP, and returns a list with all the routers
    along the shortest path.

    The source and destination IPs are **not** included in this path.

    Note that the source IP and destination IP will probably not be
    routers! They will be on the same subnet as the router. You'll have
    to search the routers to find the one on the same subnet as the
    source IP. Same for the destination IP. [Hint: make use of your
    find_router_for_ip() function from the last project!]

    The dictionary keys are router IPs, and the values are dictionaries
    with a bunch of information, including the routers that are directly
    connected to the key.

    This partial example shows that router `10.31.98.1` is connected to
    three other routers: `10.34.166.1`, `10.34.194.1`, and `10.34.46.1`:

    {
        "10.34.98.1": {
            "connections": {
                "10.34.166.1": {
                    "netmask": "/24",
                    "interface": "en0",
                    "ad": 70
                },
                "10.34.194.1": {
                    "netmask": "/24",
                    "interface": "en1",
                    "ad": 93
                },
                "10.34.46.1": {
                    "netmask": "/24",
                    "interface": "en2",
                    "ad": 64
                }
            },
            "netmask": "/24",
            "if_count": 3,
            "if_prefix": "en"
        },
        ...

    The "ad" (Administrative Distance) field is the edge weight for that
    connection.

    **Strong recommendation**: make functions to do subtasks within this
    function. Having it all built as a single wall of code is a recipe
    for madness.
    """
    
    def ip_to_value(ip):
        parts = ip.split('.')
        value = 0
        for part in parts:
            value = (value << 8) + int(part)
        return value
    
    def get_network_address(ip, netmask):
        ip_value = ip_to_value(ip)
        prefix_len = int(netmask.strip('/'))
        mask = (0xFFFFFFFF << (32 - prefix_len)) & 0xFFFFFFFF
        return ip_value & mask
    
    def find_router_for_ip(routers, target_ip):
        target_value = ip_to_value(target_ip)
        for router_ip, router_info in routers.items():
            netmask = router_info["netmask"]
            router_network = get_network_address(router_ip, netmask)
            target_network = get_network_address(target_ip, netmask)
            if router_network == target_network:
                return router_ip
        return None
    
    src_router = find_router_for_ip(routers, src_ip)
    dest_router = find_router_for_ip(routers, dest_ip)

    if src_router == dest_router:
        return []
    if src_router is None or dest_router is None:
        return []
    
    distances = {router: math.inf for router in routers}
    distances[src_router] = 0
    previous = {router: None for router in routers}
    unvisited = set(routers.keys())
    
    while unvisited:
        current = min(unvisited, key=lambda router: distances[router])
        if current == dest_router:
            break
        if distances[current] == math.inf:
            break
        unvisited.remove(current)
        for neighbor, connection_info in routers[current]["connections"].items():
            if neighbor in unvisited:
                alt_distance = distances[current] + connection_info["ad"]
                if alt_distance < distances[neighbor]:
                    distances[neighbor] = alt_distance
                    previous[neighbor] = current
    path = []
    current = dest_router
    if distances[dest_router] == math.inf:
        return []

    while current != src_router:
        path.append(current)
        current = previous[current]
        if current is None:
            return []

    path.append(src_router)
    path.reverse()
    return path

#------------------------------
# DO NOT MODIFY BELOW THIS LINE
#------------------------------
def read_routers(file_name):
    with open(file_name) as fp:
        data = fp.read()

    return json.loads(data)

def find_routes(routers, src_dest_pairs):
    for src_ip, dest_ip in src_dest_pairs:
        path = dijkstras_shortest_path(routers, src_ip, dest_ip)
        print(f"{src_ip:>15s} -> {dest_ip:<15s}  {repr(path)}")

def usage():
    print("usage: dijkstra.py infile.json", file=sys.stderr)

def main(argv):
    try:
        router_file_name = argv[1]
    except:
        usage()
        return 1

    json_data = read_routers(router_file_name)

    routers = json_data["routers"]
    routes = json_data["src-dest"]

    find_routes(routers, routes)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
    
