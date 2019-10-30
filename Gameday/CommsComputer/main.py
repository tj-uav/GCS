#from ../helpers import Connection
import json

connections = {}

def load_config(filename="config.json": str):
    return json.load(open(filename,"r"))

def create_connections():
    config = load_config()
    addresses = config["Addresses"]
    inv = {}
    num_computers = 0
    for address in addresses:
        for comp in addresses[address]:
            num_computers += 1
            inv[tuple(address)] = comp
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(addresses["Communication"])
    sock.listen(num_computers)
    connections = {}
    for i in range(num_computers):
        conn, addr = sock.accept()
        connections.get(tuple(addr),[]).append(Connection(addr[0], addr[1], conn))
    return connections

def interop_submit():

def ingest(data: dict):
    global connections
    action = data["ACTION"]
    args = data["ARGUMENTS"]
    if action == "FORWARD":
        assert(len(args) == 1)
        ip, port = args[0]
        conn = connections[(ip,port)]
        conn.enqueue(data)
    elif action == "INTEROP":
        assert(len(args) = 2)
        endpoint = args[0]
        interop_submit(endpoint)


def start():
    global connections
    connections = create_connections()
    print(connections)


if __name__ == "__main__":
    start()