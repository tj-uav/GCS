import socket
import time
import threading
from collections import deque
import json
import requests
import cv2
import base64

BUFFER = 1024
NUM_COMPUTERS = 1 #4 #3 Ground station computers, 1 jetson
JETSON_ADDR = ('127.0.0.1',8081)
MY_IP = '127.0.0.1'
PORT = 5005
CONNECTIONS = []
MESSAGE_QUEUE = deque([]) # Format for this should be (DESTINATION_IP, message)
IPS = {"COMMS_COMP":'127.0.0.1', "MISSION_PLANNER":'127.0.0.1', "JETSON": '127.0.0.1', "MANUAL_DETECTION": '127.0.0.1', "MANUAL_CLASSIFICATION": '127.0.0.1'} #Change to actual values
MISSION_ID = 1

def start():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.bind((MY_IP,PORT))
    my_socket.listen(5)
    for i in range(NUM_COMPUTERS):
        connect_device(my_socket)
    
    # COMMENTED OUT BELOW LINES FOR TESTING
#    connect_interop("http://localhost:8000", "testuser", "testpass")
#    send_mission_data()
    sending_thread = threading.Thread(target=send_data)
    sending_thread.start()

    vid_thread = threading.Thread(target=video_capture)
    vid_thread.start()

    #Create a thread for the function send_data(). Make the thread run every x milliseconds (we don't wanna spam or it might break it).

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
        time.sleep(1)
    cap.release()
    cv2.destroyAllWindows()


def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
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
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

def connect_device(sock):
    conn, addr = sock.accept()
    listen_thread = threading.Thread(target=listen_from_device, args=(conn,))
    listen_thread.start()
    ip = addr[0]
    CONNECTIONS.append((ip, conn))

def connect_interop(interop_url, username, password):
    global r, cookie_str
    r = requests.post(interop_url + "/api/login", json={"username":username, "password":password}, headers={"Content-Type":"application/json"})
    cookie_str = r.headers["Set-Cookie"].split(';')

def send_interop(message):
    print("Interop:", message)

def receive_interop(arg_name):
    global r, cookie_str
    r = requests.get("http://localhost:8000/api/" + arg_name, headers={"Cookie":cookie_str[0]})
#    print(r.text)
    return json.loads(r.text, object_hook = _decode_dict)

def send_mission_data():
    mission_data = receive_interop("missions/" + str(MISSION_ID))
    obstacle_data = receive_interop("obstacles")
    enqueue(destination=IPS['MISSION_PLANNER'], header='MISSION_DATA', message=mission_data)
    enqueue(destination=IPS['MISSION_PLANNER'], header='OBSTACLE_DATA', message=obstacle_data)


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
    if header == "TELEMETRY":
        #Save to file
        send_interop(message_dict['MESSAGE'])
        pass
    elif header == "PRINT":
        print(message_dict['MESSAGE'])
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
#            print(nextMessage)
#            for i in nextMessage['MESSAGE']:
#                print(i)
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
