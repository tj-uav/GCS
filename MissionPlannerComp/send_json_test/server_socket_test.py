import socket
ADDRESS = '10.16.188.191'

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ADDRESS, 5012))
    sock.listen()
    print("Server up")
    conn, addr = sock.accept()
    print("Connection Made")
    received = conn.recv(1024)
    print(received)

if __name__ == '__main__':
    main()    
