import socket
import json

class Connection:

    def __init__(self, ip, port, sock):
        self.ip = ip
        self.port = port
        self.connection = sock
        self.send_queue = []
        self.recv_queue = []
        self.buffer = 1024

    def enq(self, message):
        self.send_queue.append(json.dumps(message))
    
    def send(self):
        while True:
            if self.send_queue:
                message = self.send_queue.pop()
                self.sock.send(message)
    
    def receive(self):
        while True:
            data = self.sock.recv(self.buffer)
            self.ingest(json.loads(data))