import socket as sock
import time
import cv2
import numpy as np

sock = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

#binds to any open port if left blank
sock.bind(("", 5005))
sock.listen(1)
conn, addr = sock.accept()

def recvPicture(data):
    nparr = np.fromstring(data, np.uint8)
    img_decode = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imshow("img_decode", img_decode)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()

while True:
    t = time.time()
    data = conn.recv(30000)
    if len(data) > 0:
        #to receive a string
        print(str(time.time()-t)+" seconds")
        print("Length: " + str(len(data.decode("UTF-8"))))
        #to receive a picture
        #recvPicture(data)