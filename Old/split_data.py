import socket

BUFFER = 100000
address = "192.168.1.19"
port = 5005
COMPUTERS = {"192.168.1.181": "ODCL", "192.168.1.10": "ODCL", "192.168.1.29": "JETSON"}
CONNECTIONS = {"ODCL": [], "JETSON": None}
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.bind((address, port))
my_socket.listen(len(COMPUTERS))
conns = {}
for i in range(len(COMPUTERS)):
    conn, addr = my_socket.accept()
    if COMPUTERS[addr[0]] == "JETSON":
        CONNECTIONS["JETSON"] = conn
        print("Jetson connected", addr)
    else:
        CONNECTIONS["ODCL"].append(conn)
        print("ODCL connected", addr)

idx = 0
while True:
    recv_conn = CONNECTIONS["JETSON"]
    ODCL_COMPS = CONNECTIONS["ODCL"]
    data = recv_conn.recv(BUFFER)
    print(data)
    ODCL_COMPS[idx].send(data)
    idx += 1
    idx %= len(ODCL_COMPS)
