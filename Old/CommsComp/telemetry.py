import socket

class Telemetry:

    def __init__(self, ip, port, conn):
        self.ip = ip
        self.port = port
        self.connection = conn
    
    def send(self, data):
        self.connection.send(data)