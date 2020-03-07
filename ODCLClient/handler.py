import cv2
import socket
import json, pickle, base64
from threading import Thread


class Handler:
    """
    Use this class for handling all socket communication operations.
    """

    def __init__(self, config):
        self.config = config
        self.data = []
        self.images = []
        self.server_send_queue = []
        self.img_num = 1

    # Initialize the TCP socket and create a connection with each of the 
    def init_socket(self):
        self.gs_ip, self.port = self.config['gs_ip'], self.config['gs_port']
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.gs_ip, self.port))
        print("Socket successfully connected")
        self.init_threads()

    def init_threads(self):
        listen_thread = Thread(target=self.listen_server)
        listen_thread.daemon = True
        listen_thread.start()

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

    def send(self, packet):
        packet_str = json.dumps(packet).encode()
        self.sock.send(packet_str)

    def ingest_server(self, packet_str):
        packet = json.loads(packet_str.decode())
        assert (packet["header"] == "IMAGE")
        print("Received image")
        img = self.decode_img(packet["image"])
        cv2.imwrite("assets/img/submission" + str(self.img_num) + ".jpg", img)
        self.img_num += 1

    def listen_server(self):
        print("Running Server comms thread")
        while True:
            packet_str = self.sock.recv(100000)
            self.ingest_server(packet_str)

    def submit_odcl(self, filename, odcl_data):
        img = cv2.imread(filename)
        img_enc = self.encode_img(img)
        packet = {"header": "Submission", "image": img_enc, "odcl_data": odcl_data}
        self.send(packet)