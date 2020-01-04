import geopy
import geopy.distance
import socket
import threading
import time
from collections import deque   
import json

print("Importing AUVSI libraries...")
from auvsi_suas.client import client
from auvsi_suas.proto import interop_api_pb2
from google.protobuf import json_format
print("Done")

MY_IP = '127.0.0.1'
PORT = 5005
MISSION_ID = 1
global x
x = 5

def start():    
    interop_ip = "http://192.168.137.147:8000"
    user = "testuser"
    password = "testpass"
    mission_id = 1

    global cl
    cl = client.AsyncClient(interop_ip,user,password)
    print('Connected to interop')
    connect_comms()
    print('Connected to Mission Planner script')

def connect_comms():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Over Internet, TCP protocol
    sock.bind((MY_IP, PORT))
    sock.listen(1)

    conn, addr = sock.accept()

    listen_thread = threading.Thread(target=listen_from_device, args=(conn))
    listen_thread.start()

def listen_from_device(sock):
    #Constantly be listening
    #Upon receiving a message, pass it through the command_ingest
    while True:
        data_bytes = sock.recv(1024)
        data_string = data_bytes.decode("utf-8")
        data_dict = json.loads(data_string)
#        print(data_dict)
        ingest_thread = threading.Thread(target=command_ingest, args=(data_dict,))
        ingest_thread.start()
        global x
        if x == 0:
            return

def command_ingest(message_dict):
    #Interpret messages based on header and other stuff
    #Examples include: Changing the buffer value, forwarding messages to other devices, submitting to interop, etc.
    header = message_dict['HEADER']
    print(message_dict)
    if header == 'TELEMETRY':
        msg = message_dict['MESSAGE']
        print(msg)
        telemetry = interop_api_pb2.Telemetry()
        telemetry.latitude = msg['lat']
        telemetry.longitude = msg['lng']
        telemetry.altitude = msg['alt']
        telemetry.heading = msg['head']
        cl.post_telemetry(telemetry)
        print(telemetry)
        print('Submitted')


if __name__ == '__main__':
    start()
