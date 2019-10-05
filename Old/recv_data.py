import socket

BUFFER = 1000000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("192.168.1.19",5005))

num = 0
while True:
    data = sock.recv(BUFFER)
    print(num, data.decode())
    num += 1
