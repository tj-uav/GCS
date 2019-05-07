import socket
import time
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Over Internet, TCP protocol
sock.connect(('127.0.0.1', 5005))  # 127.0.0.1 refers to yourself, 5005 is arbitrary port 

"""
def request_telem():
    req_msg = "request"
    sock.send(req_msg.encode())
    print("Request for telemetry sent.")
    time.sleep(5)
"""
def listen():
    global received
    req_msg = "request"
    sock.send(req_msg.encode())
    print("Request for telemetry sent.")
    received = sock.recv(1024)

def main():
    pass


if __name__ == "__main__":
    t1 = threading.Thread(target=listen, daemon=True)
    t2 = threading.Thread(target=main, daemon=True)
