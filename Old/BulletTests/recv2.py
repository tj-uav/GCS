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

def create_blank():
   odlc = interop_api_pb2.Odlc()
   print(odlc)
   odlc.mission = 1
   odlc.type = interop_api_pb2.Odlc.STANDARD
   odlc.latitude = 50
   odlc.longitude = 50
   odlc.orientation = 1
   odlc.shape = 1
   odlc.shape_color = 1
   odlc.alphanumeric = 'A'
   odlc.alphanumeric_color = 1
   return odlc

def cv2decode(data):
    img = pickle.loads(data)
    img = cv2.imdecode(img, 1)
    return img

file = open('output.txt', 'w')
start = time.time()
HOST = '192.168.1.100'
PORT = 8485
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST,PORT))
print('Socket created')
num=0

print('Socket bind complete')
sock.listen(1)
print('Socket now listening')

conn, addr = sock.accept()

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))
file.write('Time\tFPS')
framenum = 0
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
        data += conn.recv(163840)

    frame_data = data[:msg_size]

    frame = cv2decode(frame_data)

    if framenum >= 1:
        break

    cv2.imwrite("Frame" + str(framenum) + ".png", frame)
    cv2.waitKey(1)

    framenum += 1
   
conn.close()