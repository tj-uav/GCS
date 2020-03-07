import os
import cv2
import time
import socket
import json, pickle, base64
from threading import Thread
from auvsi_suas.client import client
from auvsi_suas.proto import interop_api_pb2

"""
Use this class for handling all socket communication operations.
"""
class Handler:

    def __init__(self, config):
        self.config = config
        self.data = []
        self.images = []
        self.client_forward_queue = []
        self.submission_num = 0


    # Initialize the TCP socket and create a connection with each of the Client comps as well as the Jetson
    def init_socket(self):
        self.ip, self.port = self.config['gs_ip'], self.config['gs_port']
        self.num_client_comps = self.config['num_client_comps']
        self.total_connections = self.num_client_comps + 1 # Jetson counts as a connection
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, self.port))
        self.sock.listen(self.total_connections)
        self.client_connections = []
        self.jetson_connection = None
        for i in range(self.total_connections):
            conn, addr = self.sock.accept()
            #FIXME: This should check the address, not just assume that the first connection is w/ the Jetson
            if i == 0:
                self.jetson_connection = conn
                print("Jetson successfully connected")
            else:
                self.client_connections.append(conn)
                print("Client successfully connected")
        self.init_threads()


    def init_interop(self):
        self.interop_url = self.config['interop_url']
        self.client = client.Client(url=self.interop_url,
                        username=self.interop_username,
                        password=self.interop_password)


    def init_threads(self):
        jetson_thread = Thread(target=self.listen_jetson, args = (self.jetson_connection,))
        jetson_thread.daemon = True
        jetson_thread.start()
        print("Created jetson thread")
        
        for conn in self.client_connections:
            client_thread = Thread(target=self.listen_client, args = (conn,))
            client_thread.daemon = True
            client_thread.start()
            print("Created client thread")

        send_thread = Thread(target=self.send)
        send_thread.daemon = True
        send_thread.start()
        print("Created data sending thread")

        while True:
            pass


    def encode_img(self, img):
        _, encoded = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 80])
        encoded = pickle.dumps(encoded)
        encoded_b64 = base64.encodebytes(encoded)
        encoded_str = encoded_b64.decode('ascii')
        return encoded_str


    def decode_img(self, data):
        encoded_b64 = data.encode('ascii')
        encoded = base64.decodebytes(encoded_b64)
        img = pickle.loads(encoded)
        img = cv2.imdecode(img, 1)
        return img


    def send(self):
        assert(self.num_client_comps > 0)
        self.client_comp_idx = 0
        self.jetson_connection.send("BEGIN".encode())
        while True:
            if len(self.client_forward_queue) > 0:
                to_send = self.client_forward_queue.pop()
                conn = self.client_connections[self.client_comp_idx]
                conn.send(to_send)
                self.client_comp_idx += 1
                self.client_comp_idx %= self.num_client_comps
                time.sleep(0.2)

    def ingest_client(self, packet_str):
        packet = json.loads(packet_str.decode())
        assert (packet["header"] == "Submission")
        odcl_data = packet["odcl_data"]
        img = self.decode_img(packet["image"])
        self.submit(odcl_data, img)

    def listen_client(self, conn):
        print("Running client comms thread")
        while True:
            packet_str = conn.recv(100000)
            self.ingest_client(packet_str)


    def ingest_jetson(self, packet_str):
        packet = json.loads(packet_str.decode())
        assert (packet["image"] != None)
        if packet["header"] == "IMAGE":
            self.client_forward_queue.append(packet_str)
            print(len(self.client_forward_queue))
        else:
            print("Unknown packet header")


    def listen_jetson(self, conn):
        print("Running Jetson comms thread")
        while True:
            packet_str = conn.recv(100000)
            if len(packet_str) == 0:
                print("Communication was closed by Jetson")
                return
            self.ingest_jetson(packet_str)

    def submit(self, odcl_data, img):
        cv2.imwrite("static/submission" + str(self.submission_num) + ".jpg", img)
        print("Submission received")
        self.submission_num += 1
