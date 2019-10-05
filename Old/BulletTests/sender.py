import socket as sock
import numpy as np

def getPicture():
    import cv2
    filepath = "C:/Users/trillion33/Pictures/trillion.png"
    img = cv2.imread(filepath, 1)
    imgb = cv2.imencode('.png', img)[1]
    arr = np.array(imgb)
    return arr.tostring()

#receiving computer's ip
ip = "192.168.0.213"
#Send a string
message = ('A' * 100000000).encode("UTF-8")
#Or, to send a picture
#message = getPicture()

print('Connecting...')
socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)  # Over Internet, TCP protocol
socket.connect((ip, 5005))
print('Connected')
socket.sendall(message)
print('Sent')
