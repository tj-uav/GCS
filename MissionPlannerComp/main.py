import geopy
import geopy.distance
import socket
import threading
import time
from collections import deque
import json

from mp_help import circleToPoints, makeKmlFile

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


def connect_comms():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Over Internet, TCP protocol
    sock.connect((COMMS_IP, PORT))

    listen_thread = threading.Thread(target=listen_from_device)
    listen_thread.start()

    send_thread = threading.Thread(target=send_data)
    send_thread.start()

    telem_data_thread = threading.Thread(target=telem_data)
    telem_data_thread.start()

    time.sleep(10)
    sock.close()
    print(5/0)
    exit()

def telem_data():
    while True:
        telem = {
        'latitude': cs.lat,
        'longitude': cs.lng,
        'altitude': cs.alt,
        'heading': cs.yaw
        }

        enqueue(destination=COMMS_IP, header='TELEMETRY_DATA', message=telem)
        print("Sleeping for 0.1 seconds...")
        time.sleep(.1)

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

# from geopy.distance import vincenty

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

def testMethod():
    obstacles = [[38.861164455523,-77.4728393554688,500]]
    zoneString = "-77.4471759796143,38.8609639542521 -77.4385070800781,38.8588252388515 -77.4397945404053,38.8502697340142 -77.4490642547607,38.8519408119263"
    zoneStringPoints = zoneString.split(" ")
    zones = [[[float((z.split(",")[1])), float((z.split(",")[0]))] for z in zoneStringPoints]]
    makeKml('MissionPlannerComp/testing.kml', obstacles=obstacles, zones=zones)


def process_mission_data(mission_data):
    json_format.Parse(mission_data, mission)
    print(mission_data)
    mission_id = int(mission_data.id)
    fly_zone_data = mission_data.fly_zones
    fly_zone_pts = fly_zone_data['boundary_pts']
    home_pos = mission_data['home_pos']
    fence_pts = [home_pos] + fly_zone_pts
    print('Fence: ',fence_pts)
    obstacles_data = mission_data['stationary_obstacles']

    makeKmlFile('mission_kml.kml', , obstacles[], zones=[])
#    filename = 'mission_boundary.fen'
#    open_file(filename)
#    create_file(filename,fence_pts)
#    filename = 'obstacles.poly'
#    open_file(filename)
#    create_file(filename,obstacles_waypoints)
    
#def process_obstacle_data(mission_data):
#    obstacles_data = mission_data['stationary_obstacles']
#    obstacles_pts = []
#    for obstacle in obstacles_data:
#        obstacles_pts.append(obstacle_to_waypoints(obstacle))
#    print('Obstacles: ', obstacle_pnts)


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