# Normal package imports
import socket
import time
import threading
from collections import deque
import json
import requests
import cv2
import os

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
ODCL_SHAPECONV = {'CIRCLE' : 1, 'SEMICRICLE' : 2, 'QUARTER_CIRCLE' : 3, 'TRIANGLE' : 4, 'SQUARE' : 5, 'RECTANGLE' : 6, 'TRAPEZOID' : 7, 'PENTAGON' : 8, 'HEXAGON' : 9, 'HEPTAGON' : 10, 'OCTAGON' : 11, 'STAR' : 12, 'CROSS' : 13}
ODCL_COLORCONV = {'WHITE' : 1, 'BLACK' : 2, 'GRAY' : 3, 'RED' : 4, 'BLUE' : 5, 'GREEN' : 6, 'YELLOW' : 7, 'PURPLE' : 8, 'BROWN' : 9, 'ORANGE' : 10}
ODCL_ORIENTATIONCONV = {'N' : 1, 'NE' : 2, 'E' : 3, 'SE' : 4, 'S' : 5, 'SW' : 6, 'W' : 7, 'NW' : 8}

global cl, saved_image_num
cl = None
saved_image_num = 0

def start():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.bind((MY_IP,PORT))
    my_socket.listen(5)
    for i in range(NUM_COMPUTERS):
        connect_device(my_socket)
        print("Connection achieved")
    
    connect_interop("http://localhost:8000", "testuser", "testpass")
    # COMMENTED OUT BELOW LINES FOR TESTING
#    send_mission_data()
    sending_thread = threading.Thread(target=send_data)
    sending_thread.start()

#    vid_thread = threading.Thread(target=video_capture)
#    vid_thread.start()

def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, str):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, str):
            key = key.encode('utf-8')
        if isinstance(value, str):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

#Temporary method
def video_capture():
    cap = cv2.VideoCapture(0)
    time.sleep(1)
    while True:
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        nparr = cv2.imencode('.jpg',frame)[1]
        temp = nparr.tolist()
        print("Numpy shape:",nparr.shape)
#        img_bytes = base64.b64decode(temp).decode('utf-8')
        img_bytes = temp
        print(type(img_bytes))
        enqueue(destination=IPS['MANUAL_DETECTION'],header='CAMERA_IMAGE',message=img_bytes)
        time.sleep(0.5)
    cap.release()
    cv2.destroyAllWindows()

def connect_device(sock):
    conn, addr = sock.accept()
    listen_thread = threading.Thread(target=listen_from_device, args=(conn,))
    listen_thread.start()
    ip = addr[0]
    CONNECTIONS.append((ip, conn))

def connect_interop(interop_url, username, password):
    global cl
    cl = client.AsyncClient(url='http://127.0.0.1:8000',
                       username='testuser',
                       password='testpass')

def make_odlc_from_data(message_data):
    odlc = interop_api_pb2.Odlc()
    if 'type' in message_data and isinstance(message_data['type'], str):
        odlc.type = message_data['type']
    if 'latitude' in message_data and isinstance(message_data['latitude'], float):
        odlc.latitude = message_data['latitude']
    if 'longitude' in message_data and isinstance(message_data['longitude'], float):
        odlc.longitude = message_data['longitude']
    if 'orientation' in message_data and message_data['orientation'] in ODCL_ORIENTATIONCONV:
        odlc.orientation = ODCL_ORIENTATIONCONV['orientation']
    if 'shape' in message_data and message_data['shape'] in ODCL_SHAPECONV:
        odlc.shape = ODCL_SHAPECONV[message_data['shape']]
    if 'shape_color' in message_data and message_data['shape_color'] in ODCL_COLORCONV:
        odlc.shape_color = ODCL_COLORCONV[message_data['shape_color']]
    if 'alphanumeric' in message_data and isinstance(message_data['alphanumeric'], str):
        odlc.alphanumeric = message_data['alphanumeric']
    if 'alphanumeric_color' in message_data and message_data['alphanumeric_color'] in ODCL_COLORCONV:
        odlc.alphanumeric_color = ODCL_COLORCONV[ message_data['alphanumeric_color']]
    return odlc


def interop_handler(action, subaction, message_data=None):
    global cl
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
#        assert(type(message_data) == dict)
#        if subaction == 'ODCL':
#            odlc = make_odlc_from_data(message_data=message_data)
#            odlc = cl.post_odlc(odlc)
#            if 'image_data' in message_data and type(message_data['image_data']) == bytes:
#                cl.put_odlc_image(image_data=message_data['image_data'], odlc_id=odlc.id)
#            return odlc
        elif subaction == 'TELEMETRY':
            telemetry = interop_api_pb2.Telemetry()
            reqs = [('latitude',float), ('longitude',float), ('altitude',int), ('heading',int)]
            for req,reqtype in reqs:
                if req not in message_data or not isinstance(message_data[req], reqtype):
                    print('Telemetry reqs not satisfied')
                    return
            telemetry.latitude = message_data['latitude']
            telemetry.longitude = message_data['longitude']
            telemetry.altitude = message_data['altitude']
            telemetry.heading = message_data['heading']
            cl.post_telemetry(telemetry)
    elif action == 'PUT':
        if message_data is None:
            print('Missing message data')
            return
#        if 'ODCL_ID' not in message_data or type(message_data['ODCL_ID']) != int:
#            print('ERROR: Cannot PUT ODCL or ODCLIMAGE without valid ODCL_ID')
#            return
#        assert(type(message_data) == dict)
#        odlc_id = message_data['ODCL_ID']
#        if subaction == 'ODCL':
#            odlc = make_odlc_from_data(message_data=message_data, odlc_id=odlc_id)
#            odlc = cl.put_odlc(odlc)
#            return odlc
#        elif subaction == 'ODCLIMAGE':
#            if 'image_data' in message_data and type(message_data['image_data']) == bytes:
#            return cl.put_odlc_image(odlc_id, message_data['image_data'])
    elif action == 'GET':
        if subaction == 'MISSION':
            return cl.get_mission(MISSION_ID).result()
        elif subaction == 'ALLODCLS':
            return cl.get_odlcs(mission=MISSION_ID).result()
        else:
            if message_data is None:
                print('Missing message data')
                return
            if 'ODCL_ID' not in message_data or not isinstance(message_data['ODCL_ID'], int):
                print('ERROR: Cannot DELETE ODCL or ODCLIMAGE without valid ODCL_ID')
                return
            assert(isinstance(message_data, dict)== dict)
            odlc_id = message_data['ODCL_ID']
            if subaction == 'ODCL':
                return cl.get_odlc(odlc_id)
            elif subaction == 'ODCLIMAGE':
                return cl.get_odlc_image(odlc_id)
    elif action == 'DELETE':
        if message_data is None:
            print('Missing message data')
            return
        if 'ODCL_ID' not in message_data or not isinstance(message_data['ODCL_ID'], int):
            print('ERROR: Cannot DELETE ODCL or ODCLIMAGE without valid ODCL_ID')
            return
        assert(isinstance(message_data, dict))
        odlc_id = message_data['ODCL_ID']
        if subaction == 'ODCL':
            cl.delete_odlc(odlc_id)
        elif subaction == 'ODCLIMAGE':
            cl.delete_odlc_image(odlc_id)

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
            for c in CONNECTIONS:
                if c[0] == DESTINATION_IP:
                    conn = c[1]
                    nextMessage_json = json.dumps(nextMessage)
                    nextMessage_bytes = nextMessage_json.encode('utf-8')
                    conn.send(nextMessage_bytes)
            time.sleep(0.5) #Can be changed
            global x
            if x == 0:
                return

def listen_from_device(conn):
    #Constantly be listening
    #Upon receiving a message, pass it through the command_ingest
    while True:
        data_bytes = conn.recv(1024) 
        data_string = data_bytes.decode("utf-8")
        data_dict = json.loads(data_string)
        ingest_thread = threading.Thread(target=command_ingest, args=data_dict)
        ingest_thread.start()
        global x
        if x == 0:
            return

if __name__ == "__main__":
    start()
