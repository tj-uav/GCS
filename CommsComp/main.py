import socket
import time
import threading

BUFFER = 1024
NUM_COMPUTERS = 4 #3 Ground station computers, 1 jetson
JETSON_ADDR = ('127.0.0.1',8081)
MY_IP = '127.0.0.1'
PORT = 5005
CONNECTIONS = []
MESSAGE_QUEUE = [] # Format for this should be (DESTINATION_IP, message)

def start():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.bind((MY_IP,PORT))
    my_socket.listen(5)
    for i in range(NUM_COMPUTERS):
        connect_device(my_socket)
    
    connect_interop()
    sending_thread = threading.Thread()

    #Create a thread for the function send_data(). Make the thread run every x milliseconds (we don't wanna spam or it might break it).


def connect_device(sock):
    conn, addr = sock.accept()
    listen_thread = threading.Thread(target=listen_from_device, args=conn)
    listen_thread.start()
    ip = addr[0]
    CONNECTIONS.append((ip, conn))

def connect_interop():
    pass

def send_interop(message):
    pass

def receive_interop(args):
    pass

def command_ingest(message):
    #Interpret messages based on header and other stuff
    #Examples include: Changing the buffer value, forwarding messages to other devices, submitting to interop, etc.
    messageList = message.split(",")
    MESSAGE_QUEUE.append(messageList)

def send_data():
    #Check if MESSAGE_QUEUE is empty. If it is not empty, send that message to the corresponding device
    while MESSAGE_QUEUE:
        currentMessage = MESSAGE_QUEUE.pop(1)
        for x in range(len(CONNECTIONS)):
            if x[0] == currentMessage[0]:
                conn = x[1]
                conn.send(currentMessage[1])

def listen_from_device(conn):
    #Constantly be listening
    #Upon receiving a message, pass it through the command_ingest
    while True:
        data = conn.recv(1024) 
        if data is not None:
            break
    data = data.decode("utf-8")
    command_ingest(data)

