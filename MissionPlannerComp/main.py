import geopy
import geopy.distance
import socket
import threading
import time
from collections import deque   
import json

#External imports
from auvsi_suas.client import client
from auvsi_suas.proto import interop_api_pb2

#from auvsi_suas.client import client
#from auvsi_suas.proto import interop_api_pb2
#from google.protobuf import json_format

#from mp_help import circleToPoints, makeKmlFile

POINT_RADIUS = 15
NUM_OBSTACLE_POINTS = 10
MILES_TO_KILOMETERS = 0.62137119  # Miles to kilometers

MY_IP = '127.0.0.1'
PORT = 5005
MISSION_ID = 1
global x
x = 5

def start():
#    connect_interop("http://98.169.139.31:8000", "testuser", "testpass")
    connect_interop("http://192.168.1.102:8000", "testuser", "testpass")
    print('Connected to interop')
    connect_comms()
    print('Connected to Mission Planner script')
    process_mission_data()
    print('Created')

def connect_interop(interop_url, username, password):
    global cl
    cl = client.AsyncClient(url=interop_url,
                       username=username,
                       password=password)

def connect_comms():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Over Internet, TCP protocol
    sock.bind((MY_IP, PORT))
    sock.listen(1)

    conn, addr = sock.accept()

    listen_thread = threading.Thread(target=listen_from_device, args=(conn,))
    listen_thread.start()

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

def listen_from_device(sock):
    #Constantly be listening
    #Upon receiving a message, pass it through the command_ingest
    while True:
        data_bytes = sock.recv(1024)
        data_string = data_bytes.decode("utf-8")
        data_dict = json.loads(data_string)
        print(data_dict)
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
