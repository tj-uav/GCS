import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1',5005))
sock.listen(1)
conn,addr = sock.accept()

while True:
    data = conn.recv(10000)
    print(data)
    