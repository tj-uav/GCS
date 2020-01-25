import cv2
import io
import socket
import struct
import time
import pickle
import zlib
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.7', 8485))
# connection = client_socket.makefile('wb')

cam = cv2.VideoCapture(0)

# cam.set(3, 960)
# cam.set(4, 720)

img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
   ret, frame = cam.read()
   if ret:
      result, frame = cv2.imencode('.jpg', frame, encode_param)
      data = zlib.compress(pickle.dumps(frame, 0))
      data = pickle.dumps(frame, 0)
      size = len(data)
      print('size',size)


      #print("{}: {}".format(img_counter, size))
      client_socket.sendall(struct.pack(">L", size) + data)
      img_counter += 1

      print(img_counter)

cam.release()