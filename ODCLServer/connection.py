import socket
import threading
from collections import deque
import time
import json

class Connection:

    def __init__(self, name, conn):
        self.name = name
        self.conn = conn
        self.buffer = 1024
        self.can_send = True
        self.send_queue = deque([])
        self.ingest_queue = deque([])
    
    def send(self, header, message):
        packet = {
            "Header": header,
            "Message": message,
            "Time": time.time()
        }
        packet_str = json.dumps(packet)
        packet_enc = packet_str.encode()
        self.conn.send(packet_enc)

    def listen_thread(self):
        while True:
            data = self.conn.recv(self.buffer)
            data = data.decode()
            data = json.loads(data)
            self.ingest_queue.append(data)

    def send_thread(self):
        while True:
            if len(self.send_queue) > 0:
                if self.can_send:
                    self.conn.send(self.send_queue.popleft())
                    self.can_send = False
