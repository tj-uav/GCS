import sys
sys.path.append("C:/Python27/Lib")
sys.path.append("C:/Python27/Lib/site-packages")

import socket
import threading
import time
from collections import deque   
import json
import random

MY_IP = '127.0.0.1'
PORT = 5005
MESSAGE_QUEUE = deque([])
MISSION_ID = 1
global x
x = 5
class test():
   def __init__(self):
      self.lat = 69
      self.lng = 420
      self.alt = 69
      self.yaw = 100

def start():
    connect_comms()
    print('Connected')
    telem_data_thread = threading.Thread(target=telem_data)
    telem_data_thread.start()
    while True:
        pass

def connect_comms():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Over Internet, TCP protocol
    sock.connect((MY_IP, PORT))

    send_thread = threading.Thread(target=send_data, args=(sock))
    send_thread.start()

def telem_data():
    global cl
    cs = test()
    while True:
        packet = {}
        packet['lat'] = float(cs.lat)
        packet['lng'] = float(cs.lng)
        packet['alt'] = int(cs.alt)
        packet['head'] = int(cs.yaw)
        enqueue(header='TELEMETRY', message=packet)
        print(packet)
        time.sleep(.2)

def enqueue(header, message, subheader = None):
    to_send = {}
    to_send['SOURCE'] = MY_IP
    to_send['HEADER'] = header
    to_send['MESSAGE'] = message
    if subheader:
        to_send['SUBHEADER'] = subheader
    MESSAGE_QUEUE.append(to_send)

def send_data(sock):
    #Check if MESSAGE_QUEUE is empty. If it is not empty, send that message to the corresponding device
    while True:
        if MESSAGE_QUEUE:
            nextMessage = MESSAGE_QUEUE.popleft()
            nextMessage_json = json.dumps(nextMessage)
            nextMessage_bytes = nextMessage_json.encode('utf-8')
            sock.send(nextMessage_bytes)
            time.sleep(0.05) #Can be changed
            global x
            if x == 0:
                return

start()