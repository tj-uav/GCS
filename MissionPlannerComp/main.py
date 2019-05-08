import geopy
import geopy.distance
import socket
import threading
import time
from collections import deque
import json

NUM_OBSTACLE_POINTS = 10
MILES_TO_KILOMETERS = 0.62137119  # Miles to kilometers

COMMS_IP = '127.0.0.1'
PORT = 5005
MESSAGE_QUEUE = deque([])


def start():
    connect_comms()

#HELPER METHODS
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


def connect_comms():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Over Internet, TCP protocol
    sock.connect((COMMS_IP, PORT))

    telemetry_thread = threading.Thread(target=listen_from_device)
    telemetry_thread.start()

    telemetry_thread = threading.Thread(target=send_data)
    telemetry_thread.start()

    time.sleep(10)
    sock.close()
    print(5/0)
    exit()

def open_file(filename):
    global f
    try:
        f = open(filename, 'w+')  # Write to file, if file doesn't exist, create new
    except FileNotFoundError as e:
        print(e)

def create_file(data):
    for i in data:
        toAdd = str(i[0]) + " " + str(i[1])
        f.write(toAdd + "\n")
    f.close()


def obstacle_to_waypoints(obstacle):
    coord = [obsatcle['latitude'], obstacle['longitude']]
    radius = obstacle['radius']
    start = geopy.Point(coord[0], coord[1])
    km = (radius/5280)/MILES_TO_KILOMETERS
    dist = geopy.distance.geodesic(kilometers=km)
    obstacle_waypoints = []

    for i in range(num_points):
        bearing_interval = int(360/num_points)
        new_coord = str(dist.destination(point=start, bearing=bearing_interval*i))
        new_coord = new_coord.split(", ")
        # print(new_coord)

        first = new_coord[0].split(" ")  # North/south
        north_south = float(first[0]) + (float(first[1][0:len(first[1])-1]))/60 + \
            (float(first[2][0:len(first[2])-1]))/3600

        second = new_coord[1].split(" ")
        east_west = float(second[0]) + (float(second[1][0:len(second[1])-1]))/60 + \
            (float(second[2][0:len(second[2])-1]))/3600

        final_coord = [north_south, east_west]
        obstacle_waypoints.append(final_coord)
    return obstacle_waypoints


def process_mission_data(mission_data):
    print(mission_data)
    mission_id = int(mission_data['id'])
    fly_zone_data = mission_data['fly_zones'][0]
    fly_zone_pts = fly_zone_data['boundary_pts']
    home_pos = mission_data['home_pos']
    fence_pts = [home_pos] + fly_zone_pts
    print('Fence: ',fence_pts)
#    filename = 'mission_boundary.fen'
#    open_file(filename)
#    create_file(filename,fence_pts)
#    filename = 'obstacles.poly'
#    open_file(filename)
#    create_file(filename,obstacles_waypoints)
    
def process_obstacle_data(obstacle_data):
    obstacles_data = mission_data['stationary_obstacles']
    obstacles_pts = []
    for obstacle in obstacles_data:
        obstacles_pts.append(obstacle_to_waypoints(obstacle))
    print('Obstacles: ', obstacle_pnts)


def listen_from_device():
    #Constantly be listening
    #Upon receiving a message, pass it through the command_ingest
    while True:
        data_bytes = sock.recv(102400)
        print('GOTTEM')
        data_string = data_bytes.decode("utf-8")
        data_dict = json.loads(data_string, object_hook = _decode_dict)
        command_ingest(data_dict)
        break

def command_ingest(message_dict):
    #Interpret messages based on header and other stuff
    #Examples include: Changing the buffer value, forwarding messages to other devices, submitting to interop, etc.
    header = message_dict['HEADER']
    if header == 'MISSION_DATA':
        process_mission_data(message_dict['MESSAGE'])
    elif header == 'OBSTACLE_DATA':
        process_obstacle_data(message_dict['MESSAGE'])

def enqueue(destination, header, message, subheader = None):
    to_send = {}
    to_send['SOURCE'] = MY_IP
    to_send['DESTINATION'] = destination
    to_send['HEADER'] = header
    to_send['MESSAGE'] = message
    if subheader:
        to_send['SUBHEADER'] = subheader
    MESSAGE_QUEUE.append(to_send)

def send_data():
    #Check if MESSAGE_QUEUE is empty. If it is not empty, send that message to the corresponding device
    if True:
        if MESSAGE_QUEUE:
            nextMessage = MESSAGE_QUEUE.popleft()
            DESTINATION_IP = nextMessage['DESTINATION']
            nextMessage_json = json.dumps(nextMessage)
            nextMessage_bytes = nextMessage_json.encode('utf-8')
            sock.send(nextMessage_bytes)
            time.sleep(0.05) #Can be changed

if __name__ == '__main__':
    start()