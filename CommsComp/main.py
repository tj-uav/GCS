# Normal package imports
import socket
import time
import threading
from collections import deque
import json
import requests
import cv2
import os

# Self-declared package imports
from ../helpers/comms_help import _decode_list, _decode_dict, video_capture

# AUVSI imports
from auvsi_suas.client import client
from auvsi_suas.proto import interop_api_pb2

BUFFER = 1024
NUM_COMPUTERS = 1 #4 #3 Ground station computers, 1 jetson
CONNECTIONS = []
MESSAGE_QUEUE = deque([]) # Format for this should be dictionary
IPS = {"COMMS_COMP":'127.0.0.1', "MISSION_PLANNER":'127.0.0.1', "JETSON": '127.0.0.1', "MANUAL_DETECTION": '127.0.0.1', "MANUAL_CLASSIFICATION": '127.0.0.1'} #Change to actual values
MY_IP = IPS["COMMS_COMP"]
PORT = 5005
MISSION_ID = 1
#BASE_URL = "http://localhost:8000/api/"
ODCL_IDS = {}
ALLACTIONS = {'GET': ['MISSION', 'ALLODCLS', 'ODCL', 'ODCLIMAGE'], 'POST': ['ODCL', 'TELEMETRY'], 'PUT': ['ODCL', 'ODCLIMAGE'], 'DELETE': ['ODCL, ODCLIMAGE']}
global client, saved_image_num
client = None
saved_image_num = 0

def start():
#    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#    my_socket.bind((MY_IP,PORT))
#    my_socket.listen(5)
#    for i in range(NUM_COMPUTERS):
#        connect_device(my_socket)
#        print("Connection achieved")
    
    connect_interop("http://localhost:8000", "testuser", "testpass")
    # COMMENTED OUT BELOW LINES FOR TESTING
#    send_mission_data()
#    sending_thread = threading.Thread(target=send_data)
#    sending_thread.start()

#    vid_thread = threading.Thread(target=video_capture)
#    vid_thread.start()

def connect_device(sock):
    conn, addr = sock.accept()
    listen_thread = threading.Thread(target=listen_from_device, args=(conn,))
    listen_thread.start()
    ip = addr[0]
    CONNECTIONS.append((ip, conn))

def connect_interop(interop_url, username, password):
    global client
    client = client.Client(url='http://127.0.0.1:8000',
                       username='testuser',
                       password='testpass')

def make_odlc_from_data():
    odlc = interop_api_pb2.Odlc()
    if 'type' in message_data and type(message_data['type']) == str:
        odlc.type = message_data['type']
    if 'latitude' in message_data and type(message_data['latitude']) == float:
        odlc.latitude = message_data['latitude']
    if 'longitude' in message_data and type(message_data['longitude']) == float:
        odlc.longitude = message_data['longitude']
    if 'orientation' in message_data and message_data['orientation'] in ODCL_ORIENTATIONCONV:
        odlc.orientation = ODCL_ORIENTATIONCONV['orientation']
    if 'shape' in message_data and message_data['shape'] in ODCL_SHAPECONV:
        odlc.shape = ODCL_SHAPECONV[message_data['shape']]
    if 'shape_color' in message_data and message_data['shape_color'] in ODCL_COLORCONV:
        odlc.shape_color = ODCL_COLORCONV[message_data['shape_color']]
    if 'alphanumeric' in message_data and type(message_data['alphanumeric']) == str:
        odlc.alphanumeric = message_data['alphanumeric']
    if 'alphanumeric_color' in message_data and message_data['alphanumeric_color'] in ODCL_COLORCONV:
        odlc.alphanumeric_color =ODCL_COLORCONV[ message_data['alphanumeric_color']]
    return odlc

def interop_handler(action, subaction, message_data=None):
    if action not in ALLACTIONS:
        print("Action not found")
        return
    if subaction not in ALLACTIONS[action]:
        print("Sub-action not found")
        return
    if action == 'POST':
        if message_data is None:
            print('Missing message data')
            return
        assert(type(message_data) == dict)
        if subaction == 'ODCL':
            odlc = make_odlc_from_data(odlc)
            odlc = client.post_odlc(odlc)
            if 'image_data' in message_data and type(message_data['image_data']) == bytes:
                client.put_odlc_image(odlc.id, message_data['image_data'])
            return odlc
        elif subaction == 'TELEMETRY':
            telemetry = interop_api_pb2.Telemetry()
            reqs = [('latitude',float), ('longitude',float), ('altitude',int), ('heading',int)]
            for req,reqtype in reqs:
                if req not in message_data or type(message_data[req]) != reqtype:
                    print('Telemetry reqs not satisfied')
                    return
            telemetry.latitude = message_data['latitude']
            telemetry.longitude = message_data['longitude']
            telemetry.altitude = message_data['altitude']
            telemetry.heading = message_data['heading']
            client.post_telemetry(telemetry)
    elif action == 'PUT':
        if message_data is None:
            print('Missing message data')
            return
        if 'ODCL_ID' not in message_data or type(message_data['ODCL_ID']) != int:
            print('ERROR: Cannot PUT ODCL or ODCLIMAGE without valid ODCL_ID')
            return
        assert(type(message_data) == dict)
        odlc_id = message_data['ODCL_ID']
        if subaction == 'ODCL':
            odlc = make_odlc_from_data(odlc_id, odlc)
            odlc = client.put_odlc(odlc)
            return odlc
        elif subaction == 'ODCLIMAGE':
            if 'image_data' in message_data and type(message_data['image_data']) == bytes:
                return client.put_odlc_image(odlc_id, message_data['image_data'])
    elif action == 'GET':
        if subaction == 'MISSION':
            return client.get_mission(MISSION_ID)
        elif subaction == 'ALLODCLS':
            return client.get_odlcs(mission=MISSION_ID)
        else:
            if message_data is None:
                print('Missing message data')
                return
            if 'ODCL_ID' not in message_data or type(message_data['ODCL_ID']) != int:
                print('ERROR: Cannot DELETE ODCL or ODCLIMAGE without valid ODCL_ID')
                return
            assert(type(message_data) == dict)
            odlc_id = message_data['ODCL_ID']
            if subaction == 'ODCL':
                return client.get_odlc(odlc_id)
            elif subaction == 'ODCLIMAGE':
                return client.get_odlc_image(odlc_id)
    elif action == 'DELETE':
        if message_data is None:
            print('Missing message data')
            return
        if 'ODCL_ID' not in message_data or type(message_data['ODCL_ID']) != int:
            print('ERROR: Cannot DELETE ODCL or ODCLIMAGE without valid ODCL_ID')
            return
        assert(type(message_data) == dict)
        odlc_id = message_data['ODCL_ID']
        if subaction == 'ODCL':
            client.delete_odlc(odlc_id)
        elif subaction == 'ODCLIMAGE':
            client.delete_odlc_image(odlc_id)

def enqueue(destination, header, message, subheader = None):
#    print(message)
    to_send = {}
    to_send['SOURCE'] = MY_IP
    to_send['DESTINATION'] = destination
    to_send['HEADER'] = header
    to_send['MESSAGE'] = message
    if subheader:
        to_send['SUBHEADER'] = subheader
    MESSAGE_QUEUE.append(to_send)

def my_ingest(message_dict):
    header = message_dict['HEADER']
    message = message_dict['MESSAGE']
    if header == 'INTEROP':
        if 'subheader' not in message_dict:
            print('Missing Subheader for Interop message')
            return
        (action,subaction) = message_dict['subheader'].split(" ")
        interop_handler(action, subaction, message)
    elif header == "PRINT":
        print(message_dict['MESSAGE'])
    elif header == "TERMINATE":
        os._exit(1)
    else:
        print('Unknown header:',header)

def command_ingest(message_dict):
    #Interpret messages based on header and other stuff
    #Examples include: Changing the buffer value, forwarding messages to other devices, submitting to interop, etc.
    DESTINATION_IP = message_dict['DESTINATION']
    if DESTINATION_IP == MY_IP:
        my_ingest(message_dict)
    else:
        MESSAGE_QUEUE.append(message_dict)

def send_data():
    #Check if MESSAGE_QUEUE is empty. If it is not empty, send that message to the corresponding device
    while True:
        if MESSAGE_QUEUE:
            nextMessage = MESSAGE_QUEUE.popleft()
            DESTINATION_IP = nextMessage['DESTINATION']
            print(type(nextMessage))
            for x in CONNECTIONS:
                if x[0] == DESTINATION_IP:
                    conn = x[1]
                    nextMessage_json = json.dumps(nextMessage)
                    nextMessage_bytes = nextMessage_json.encode('utf-8')
                    conn.send(nextMessage_bytes)
            time.sleep(0.5) #Can be changed

def listen_from_device(conn):
    #Constantly be listening
    #Upon receiving a message, pass it through the command_ingest
    while True:
        data_bytes = conn.recv(1024) 
        data_string = data_bytes.decode("utf-8")
        data_dict = json.loads(data_string)
        ingest_thread = threading.Thread(target=command_ingest, args=data_dict)
        ingest_thread.start()

if __name__ == "__main__":
    start()
