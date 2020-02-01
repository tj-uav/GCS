import zlib
import pickle
import socket
import struct
import threading

#ODCL_COMPS = ['0.0.0.0', '1.1.1.1', '2.2.2.2'] # replace with IP addresses of ODCL comps
ODCL_COMPS = ['127.0.0.1', '127.0.0.1', '127.0.0.1'] # replace with IP addresses of ODCL comps
ODCL_PORTS = [5000, 5005, 5010] # replace with ports to connect to on each ODCL comp
DISH_IP = '127.0.0.1'
DISH_PORT = 5010

current_target = None
img_count = 0

data = []

def start_connections():
    global dish_sock, odcl_one_sock, odcl_two_sock
    dish_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dish_sock.connect((DISH_IP, DISH_PORT))
    recv_thread = threading.Thread(target=recieve_data)
    recv_thread.daemon = True
    recv_thread.start()

    odcl_one_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    odcl_one_sock.connect((ODCL_COMPS[0], ODCL_PORTS[0]))
    trans_thread = threading.Thread(target=transmit_data)
    trans_thread.daemon = True
    trans_thread.start()

    odcl_two_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    odcl_two_sock.connect((ODCL_COMPS[1], ODCL_PORTS[1]))
    trans_thread = threading.Thread(target=transmit_data)
    trans_thread.daemon = True
    trans_thread.start()

    odcl_three_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    odcl_three_sock.connect((ODCL_COMPS[2], ODCL_PORTS[1]))
    trans_thread = threading.Thread(target=transmit_data)
    trans_thread.daemon = True
    trans_thread.start()


def distribute_images():
    global trans_sock
    compressed_image = read_compressed_image()
    if(img_count % 3 == 0):
        odcl_one_sock.send(compressed_image)
    elif(img_count % 3 == 1):
        odcl_two_sock.send(compressed_image)
    else:
        odcl_three_sock.send(compressed_image)

    img_count += 1


# Should return compressed image data
def read_compressed_image():
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
    return frame
