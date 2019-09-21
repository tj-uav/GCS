import cv2
import io
import socket
import struct
import time
import pickle
import zlib

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.1.100",8485))

cam = cv2.VideoCapture(0)

cam.set(3, 960)
cam.set(4, 720)

counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    ret, frame = cam.read()
    if ret:
        result, frame = cv2.imencode('.jpg', frame, encode_param)
        data = pickle.dumps(frame, 0)
        size = len(data)

        print("{}: {}".format(counter, size))
        client.sendall(struct.pack(">L", size) + data)
        counter += 1

cam.release()