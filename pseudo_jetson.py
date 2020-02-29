import os
import cv2
import time
import json
import socket
import pickle
import base64

cap = cv2.VideoCapture(0)
#filepath = "jetson_imgs/"
#files = os.listdir(filepath)
config = json.load(open("ODCLServer/config.json"))
gs_ip, gs_port = config["gs_ip"], config["gs_port"]
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((gs_ip, gs_port))

wait = sock.recv(1024)

def encode_img(img):
    print(img.shape)
    _, encoded = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 80])
    encoded = pickle.dumps(encoded)
    encoded_b64 = base64.encodebytes(encoded)
    encoded_str = encoded_b64.decode('ascii')
    return encoded_str

while cap.isOpened():
#for file in files:
#    img = cv2.imread(filepath + file)
    ret, img = cap.read()
    if ret == False:
        continue
    enc_img = encode_img(img)
    packet = {"header":"IMAGE", "image":enc_img}
    packet_str = json.dumps(packet).encode()
    sock.send(packet_str)
    time.sleep(0.5)

print("Cap closed")
cap.release()

while True:
    pass