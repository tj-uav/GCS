import socket
import cv2
import json, pickle, base64
import time
import os

from auvsi_suas.client import client
from auvsi_suas.proto import interop_api_pb2

"""
Use this class for handling all socket communication operations.
"""
class Handler:

    def __init__(self, config):
        self.config = config

    # Initialize the TCP socket and create a connection with each of the 
    def init_socket(self):
        self.ip, self.port = self.config['gs_ip'], self.config['gs_port']
        self.num_odcl_comps = self.config['num_odcl_comps']
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, self.port))
        self.sock.listen(self.num_odcl_comps)
        self.connections = []
        for i in range(self.num_odcl_comps):
            conn, addr = sock.accept()
            self.connections.append(conn)

    def init_interop(self, config):
        self.interop_url = self.config['interop_url']
        self.client = client.Client(url=self.interop_url,
                        username=self.interop_username,
                        password=self.interop_password)


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


    def save_image(self, conn):
        print("Running image saving thread")
        img_num = 1
        while True:
            packet_str = conn.recv(100000)
            print("Packet: ", packet_str)
            packet = json.loads(packet_str.decode())
            odcl_data = packet["odcl_data"]
            img = self.decode_img(packet["image"])
            cv2.imwrite("static/submission" + str(img_num) + ".jpg", img)
            print("WROTE THE IMAGE TO static/submission" + str(img_num) + ".jpg")
            img_num += 1

    def send_image(self, filename):
        print(filename)
        img = cv2.imread("jetson_imgs/" + filename)
        encoded = base64.encodebytes(encode_img(img))
        packet = {"header": "IMAGE", "image": encoded.decode('ascii'), "odcl_data": {}}
        packet_str = json.dumps(packet)
        self.conn.send(packet_str)


    def jetson_update(self):
        time.sleep(2)
        distributed_imgs = {}
        while True:
            for filename in os.listdir(os.path.abspath('jetson_imgs')):
                if filename in distributed_imgs:
                    continue
                if filename.endswith(".png") or filename.endswith(".jpg"):
                    print("Sending " + filename + "...")
                    time.sleep(0.25)
                    self.send_image(filename)
                    print(filename + " sent!")
                    time.sleep(0.25)
                    distributed_imgs.add(filename)


    def submit_to_interop(self, odcl_dict):
        odlc = interop_api_pb2.Odlc()
        odlc.type = interop_api_pb2.Odlc.STANDARD
        odlc.latitude = odcl_dict["latitude"]
        odlc.longitude = odcl_dict["longitude"]
        odlc.orientation = odcl_dict["orientation"]
        odlc.shape = odcl_dict["shape"]
        odlc.shape_color = odcl_dict["shape_color"]
        odlc.alphanumeric = odcl_dict["alphanumeric"]
        odlc.alphanumeric_color = odcl_dict["alphanumeric_color"]

        odlc = client.post_odlc(odlc)

        with open(odcl_dict["img_path"], 'rb') as f:
            image_data = f.read()
            client.put_odlc_image(odlc.id, image_data)
