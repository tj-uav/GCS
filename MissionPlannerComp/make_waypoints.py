from auvsi_suas.proto import interop_api_pb2
from auvsi_suas.client import client
import json
from google.protobuf import json_format
import sys
import mp_help

interop_ip = "http://192.168.137.147:8000"
user = "testuser"
password = "testpass"
mission_id = 1

mission_obj = interop_help.getMissionObj(interop_ip, user, password, mission_id)
points, obstacles, zones, waypoints = interop_help.processMission(mission_obj)

try:
    mp_help.makeKmlFile('mission_kml.kml', points, obstacles, zones)
    print("KML saved to mission_kml.kml")
except:
    print("Couldn't make KML!")
    print(sys.exc_info()[0])

try:
    mp_help.makeWpFile('mission.waypoints', waypoints)
    print("Waypoints saved to mission.waypoints")
except:
    print("Couldn't make waypoints!")
    print(sys.exc_info()[0])