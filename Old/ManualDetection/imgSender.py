import socket as s
import cv2
import os
from os import listdir
from os.path import isfile, join
import numpy as np


folder = "C:/Users/Ganes/Pictures/"
sock = s.socket(s.AF_INET, s.SOCK_STREAM)

input("Enter to continue")
print("E to exit \nS to send\n")

sock.connect(("127.0.0.1", 5005))

pics = [f for f in listdir(folder) if isfile(join(folder, f))]

for i in pics:
    inp = input("")
    if inp is "E":
        break
    if inp is "S":
        img = cv2.imread(folder+i)
        sock.sendall(cv2.imencode('.jpg', img)[1].tostring())