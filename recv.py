# from auvsi_suas.client import client
# from auvsi_suas.proto import interop_api_pb2
# from google.protobuf import json_format

# cl = client.AsyncClient(url="http://192.168.1.108:8000", username="testuser", password="testpass")

import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import time
import zlib

file = open('output.txt', 'w')
oldtime = time.time()
HOST = ''
PORT = 8485
num = 0

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')
sock.bind((HOST,PORT))
print('Socket bind complete')
sock.listen(1)
print('Socket now listening')

conn, addr = sock.accept()

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))
file.write('Time\tFPS')
t0 = time.time()
while True:
    while len(data) < payload_size:
        print("Recv: {}".format(len(data)))
        data += conn.recv(4096)

    print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: {}".format(msg_size))

    while len(data) < msg_size:
        data += conn.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    cv2.imshow("img", frame)
    cv2.waitKey(1)

