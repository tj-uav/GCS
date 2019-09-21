import socket

BUFFER = 100000
COMPUTERS = {:"ODCL", ip:"ODCL", ip:"JETSON"}
CONNECTIONS = {"ODCL":[], "JETSON":None}
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.bind((address,port))
my_socket.listen(len(COMPUTERS))
conns = {}
for i in range(len(COMPUTERS)):
    conn, addr = my_socket.accept()
    if COMPUTERS[addr] == "JETSON":
        CONNECTIONS["JETSON"] =  conn
    else:
        CONNECTIONS["ODCL"].append(conn)

idx = 0
while True:
    recv_conn = CONNECTIONS["JETSON"]
    ODCL_COMPS = CONNECTIONS["ODCL"]
    data = recv_conn.recv(BUFFER)
    ODCL_COMPS[idx].send(data)
    idx += 1
    idx %= len(ODCL_COMPS)

