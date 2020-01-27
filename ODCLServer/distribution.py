import zlib
import pickle
import socket
import struct
import threading

#ODCL_COMPS = ['0.0.0.0', '1.1.1.1', '2.2.2.2'] # replace with IP addresses of ODCL comps
ODCL_COMPS = ['127.0.0.1', '127.0.0.1'] # replace with IP addresses of ODCL comps
ODCL_PORTS = [5000, 5005] # replace with ports to connect to on each ODCL comp
DISH_IP = '127.0.0.1'
DISH_PORT = 5010
MY_IP = '127.0.0.1'

current_target = None
img_count = 0

data = []

def start_connections():
    global dish_sock, router_sock
    dish_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dish_sock.connect((DISH_IP, DISH_PORT))
    recv_thread = threading.Thread(target=recieve_data)
    recv_thread.daemon = True
    recv_thread.start()

    router_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    router_sock.connect((server_url, port))
    trans_thread = threading.Thread(target=transmit_data)
    trans_thread.daemon = True
    trans_thread.start()

def determine_target():
    current_target = ODCL_comps[img_count % 3]


def transmit_data(frame):
    global trans_sock
    data = zlib.compress(pickle.dumps(frame, 0))
    data = pickle.dumps(frame, 0)
    trans_sock.sendall(struct.pack(">L", len(data)) + data)


def recieve_data():
    global recv_sock


def recieve():
    data = b""
    payload_size = struct.calcsize(">L")
    print("payload_size: {}".format(payload_size))
    fil.write('Time\tFPS')
    t0 = time.time()

    while len(data) < payload_size:
        print("Recv: {}".format(len(data)))
        data += conn.recv(4096)
    print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: {}".format(msg_size))
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
