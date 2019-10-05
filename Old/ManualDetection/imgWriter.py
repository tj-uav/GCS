import socket as sock
import cv2
import numpy as np
import random

s = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
s.bind(("127.0.0.1", 5005))
folder = "assets/img/"

s.listen(1)
co, add = s.accept()
def save_image(img):
    cv2.imwrite(folder + str(random.randint(0,1000))+".jpg", img)

while True:
        raw = co.recv(1000000)
        arr = np.fromstring(raw, np.uint8)
        save_image(cv2.imdecode(arr, cv2.IMREAD_COLOR))

