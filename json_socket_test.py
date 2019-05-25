import socket

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('192.168.86.135', 5012))
    sock.listen()
    print("Server up")
    conn, addr = sock.accept()
    print("Connection Made")
    received = conn.recv(1024)
    print(received)

if __name__ == '__main__':
    main()    