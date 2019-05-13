import socket as s
import cv2
import os
from os import listdir
print("E to exit \nS to send")
folder = "C:/Users/Ganes/Pictures/"
sock = s.socket(s.AF_INET, s.SOCK_STREAM)

input("wait")

sock.connect(("127.0.0.1", 5005))

pics = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for i in pics:
    inp = input("")
    if inp is "E":
        break
    if inp is "S":
        img = cv2.imread(folder+i)
        sock.sendall(cv2.imencode('.jpg', img)[1].tostring())