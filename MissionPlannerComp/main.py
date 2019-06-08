import sys
#print(sys.path)
#from google.protobuf import json_format
sys.path.append("C:/Python27/Lib")
sys.path.append("C:/Python27/Lib/site-packages")
sys.path.append("C:/Python27/Lib/site-packages/google")
sys.path.append("C:/Python27/Lib/site-packages/google/protobuf")
sys.path.append("E:/Jason/UAV/interop/client")
#import google.protobuf.json_format
#to_import = [ 'E:/Jason/UAV/interop/client', 'C:/WINDOWS/SYSTEM32/python27.zip', 'C:/Python27/DLLs', 'C:/Python27/lib',
#    'C:/Python27/lib/plat-win', 'C:/Python27/lib/lib-tk', 'C:/Python27', 'C:/Python27/lib/site-packages']
#for path in to_import:
#    sys.path.append(path)
print('Started importing')
print(sys.path)
#import google
#import json_format
#from google.protobuf import json_format
import geopy
import geopy.distance
import socket
import threading
import time
from collections import deque   
import json
print('Almost done')

from auvsi_suas.client import client
from auvsi_suas.proto import interop_api_pb2
print('Done Importing')

#from auvsi_suas.client import client
#from auvsi_suas.proto import interop_api_pb2
#from google.protobuf import json_format

#from mp_help import circleToPoints, makeKmlFile

POINT_RADIUS = 15
NUM_OBSTACLE_POINTS = 10
MILES_TO_KILOMETERS = 0.62137119  # Miles to kilometers

MY_IP = '127.0.0.1'
ODCL_IP = '127.0.0.1'
PORT = 5005
MESSAGE_QUEUE = deque([])
MISSION_ID = 1
global x
x = 5

def start():
    connect_interop("http://98.169.139.31:8000", "testuser", "testpass")
    print('Connected')
    process_mission_data()
    print('Created')

#HELPER METHODS
def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        else:
            item = item.encode('utf-8')
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        else:
            key = key.encode('utf-8')
            value = key.encode('utf-8')
#        if isinstance(key, unicode):
#            key = key.encode('utf-8')
#        if isinstance(value, unicode):
#            value = value.encode('utf-8')
#        elif isinstance(value, list):
#            value = _decode_list(value)
#        elif isinstance(value, dict):
#            value = _decode_dict(value)
        rv[key] = value
    return rv

def connect_interop(interop_url, username, password):
    global cl
    cl = client.AsyncClient(url=interop_url,
                       username=username,
                       password=password)

"""
def connect_comms():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Over Internet, TCP protocol
    sock.connect((COMMS_IP, PORT))

    listen_thread = threading.Thread(target=listen_from_device, args=(sock,))
    listen_thread.start()

    send_thread = threading.Thread(target=send_data, args=(sock,))
    send_thread.start()

    time.sleep(2)
    print('Requesting Mission')
    enqueue(destination=COMMS_IP, header='INTEROP', subheader='GET MISSION', message={})

#    telem_data_thread = threading.Thread(target=telem_data)
#    telem_data_thread.start()
    time.sleep(4)
    global x
    x = 0
    sock.close()
    exit()
"""

def telem_data():
    global cl
    while True:
        telemetry = interop_api_pb2.Telemetry()
        telemetry.altitude = cs.lat
        telemetry.longitude = cs.lng
        telemetry.alt = cs.alt
        telemetry.heading = cs.yaw
#        enqueue(destination=COMMS_IP, header='TELEMETRY_DATA', message=telem)
        cl.post_telemetry(telemetry)
        print("Sleeping for 0.1 seconds...")
        time.sleep(.1)

#Radius assumes feet
def circleToPoints(centerx, centery, radius, num_points=40):
    POINT_RADIUS = 15
    CONSTANT = 0.62137119  # Miles to kilometers

    start = geopy.Point(centerx, centery)
    radius_km = (radius/5280)/CONSTANT
    dist = geopy.distance.geodesic(kilometers=radius_km)
    circlePoints = []

    for i in range(num_points):
        bearing_interval = int(360/num_points)
        new_coord = str(dist.destination(point=start, bearing=bearing_interval*i))
        new_coord = new_coord.split(", ")
        # print(new_coord)

        first = new_coord[0].split(" ")  # North/south
        north_south = float(first[0]) + (float(first[1][0:len(first[1])-1]))/60 + \
            (float(first[2][0:len(first[2])-1]))/3600
        
        if first[len(first)-1].strip() == "S":
            north_south *= -1

        second = new_coord[1].split(" ")
        east_west = float(second[0]) + (float(second[1][0:len(second[1])-1]))/60 + \
            (float(second[2][0:len(second[2])-1]))/3600

        if second[len(first)-1].strip() == "W":
            east_west *= -1

        final_coords = [north_south, east_west]
        circlePoints.append(final_coords)
    return circlePoints

def KmlBeginning():
    return """<?xml version="1.0" encoding="utf-8" ?>
    <kml xmlns="http://www.opengis.net/kml/2.2">
    <Document id="root_doc">
    <Folder><name>test</name>
    <Placemark>
	<name>polygon1</name>
	<Style><LineStyle><color>ffffffff</color></LineStyle><PolyStyle><fill>1</fill></PolyStyle></Style>
    <MultiGeometry>
    """

def KmlEnding():
    return """
    </MultiGeometry>
    </Placemark>
    </Folder>
    </Document>
    </kml>
    """

def KmlPolygon(points):
    string = """
    <Polygon>
    <outerBoundaryIs><LinearRing><coordinates>
    """
    for point in points:
        [a,b] = point
        string += str(b) + "," + str(a) + "\n"
    string += """
    </coordinates></LinearRing></outerBoundaryIs>
    </Polygon>
    """
    return string

def makeKmlFile(filename, points=[], obstacles=[], zones=[]):
    KMLSTRING = ""
    KMLSTRING += KmlBeginning()
    for point in points:
        toAdd = circleToPoints(point[0], point[1], POINT_RADIUS)
        KMLSTRING += KmlPolygon(toAdd)
    for obstacle in obstacles:
        toAdd = circleToPoints(obstacle[0], obstacle[1], obstacle[2])
        KMLSTRING += KmlPolygon(toAdd)
    for zone in zones:
        KMLSTRING += KmlPolygon(zone)
    KMLSTRING += KmlEnding()
    with open(filename, 'w+') as file:
        file.write(KMLSTRING)
        file.close()

def process_mission_data():
    global cl
    mission_obj = cl.get_mission(MISSION_ID).result()

    fly_zone_data = mission_obj.fly_zones[0]
    fence_pts = []
    for pt in fly_zone_data.boundary_points:
        fence_pts.append((pt.latitude,pt.longitude))
    maxAlt = fly_zone_data.altitude_max
    minAlt = fly_zone_data.altitude_min

    grid_pts = []
    for pt in mission_obj.search_grid_points:
        grid_pts.append((pt.latitude, pt.longitude))

    waypoints = []
    for pt in mission_obj.waypoints:
        waypoints.append((pt.latitude, pt.longitude, pt.altitude))

    obstacles_data = mission_obj.stationary_obstacles
    obstacles = []
    for obs in obstacles_data:
        obstacles.append((obs.latitude, obs.longitude, obs.radius))

    airDropPos_data = mission_obj.air_drop_pos
    airDropPos = (airDropPos_data.latitude, airDropPos_data.longitude)
    offAxisPos_data = mission_obj.off_axis_odlc_pos
    offAxisPos = (offAxisPos_data.latitude, offAxisPos_data.longitude)
    emergentPos_data = mission_obj.emergent_last_known_pos
    emergentPos = (emergentPos_data.latitude, emergentPos_data.longitude)
    
    points_to_draw = [airDropPos, offAxisPos, emergentPos] + waypoints

    makeKmlFile('mission_kml.kml', points=points_to_draw, obstacles=obstacles, zones=[grid_pts, fence_pts])
#    filename = 'mission_boundary.fen'
#    open_file(filename)
#    create_file(filename,fence_pts)
#    filename = 'obstacles.poly'
#    open_file(filename)
#    create_file(filename,obstacles_waypoints)

"""
def listen_from_device(sock):
    #Constantly be listening
    #Upon receiving a message, pass it through the command_ingest
    while True:
        data_bytes = sock.recv(10240)
        data_string = data_bytes.decode("utf-8")
        data_dict = json.loads(data_string)
        ingest_thread = threading.Thread(target=command_ingest, args=(data_dict,))
        ingest_thread.start()
        global x
        if x == 0:
            return

def command_ingest(message_dict):
    #Interpret messages based on header and other stuff
    #Examples include: Changing the buffer value, forwarding messages to other devices, submitting to interop, etc.
    header = message_dict['HEADER']
    if header == 'MISSION_DATA':
        process_mission_data(message_dict['MESSAGE'])

def enqueue(destination, header, message, subheader = None):
    to_send = {}
    to_send['SOURCE'] = MY_IP
    to_send['DESTINATION'] = destination
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
            DESTINATION_IP = nextMessage['DESTINATION']
            nextMessage_json = json.dumps(nextMessage)
            nextMessage_bytes = nextMessage_json.encode('utf-8')
            sock.send(nextMessage_bytes)
            time.sleep(0.05) #Can be changed
            global x
            if x == 0:
                return
"""
if __name__ == '__main__':
    start()