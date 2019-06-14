from auvsi_suas.proto import interop_api_pb2
from auvsi_suas.client import client
import json
from google.protobuf import json_format

cl = client.AsyncClient("http://192.168.137.147:8000", "testuser", "testpass")#http://10.10.130.10:80", 'jefferson', "8450259628")
arr = cl.get_mission(1).result()

count = 0

hlat = 0
hlon = 0

#for i in arr:
 #   if i is "waypoints":
  #      lat = str(arr.waypoints[count]["latitude"])
   #     lon = str(arr.waypoints[count]["longitude"])
    #    alt = str(arr.waypoints[count]["altitude"])
     #   print(str(count)+"\t0\t0\t16\t0\t0\t0\t0\t"+lat+"\t"+lon+"\t"+alt)
        

mission_obj = arr

fly_zone_data = mission_obj.fly_zones[0]
fence_pts = []
for pt in fly_zone_data.boundary_points:
    fence_pts.append((pt.latitude,pt.longitude))
maxAlt = fly_zone_data.altitude_max
minAlt = fly_zone_data.altitude_min

grid_pts = []
for pt in mission_obj.search_grid_points:
    grid_pts.append((pt.latitude, pt.longitude))

waypoints = mission_obj.waypoints
#for pt in mission_obj.waypoints:
#    waypoints.append((pt.latitude, pt.longitude, pt.altitude))

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

#points_to_draw = [airDropPos, offAxisPos, emergentPos] + waypoints

#makeKmlFile('mission_kml.kml', points=points_to_draw, obstacles=obstacles, zones=[grid_pts, fence_pts])


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

def makeWpFile(filename, arr):
    write = open(filename, "w+")
    count = 0
    write.write("QGC WPL 110\n")#0\t1\t0\t16\t0\t0\t0\t38.881657\t-77.260719\t118.669998\n")
    
    print(arr)
    for wp in arr:
        count += 1
        write.write(str(count) + "\t0\t0\t16\t0.00000000\t0.00000000\t0.00000000\t0.00000000\t" + str(wp.latitude) + "\t" + str(wp.longitude) + "\t" + str(wp.altitude) + "\t1\n")

    write.write(str(count+1)+"\t0\t3\t183\t2.000000\t988.000000\t0.000000\t0.000000\t0.000000\t0.000000\t0.000000\t1\n"+
    str(count+2) + "\t0\t3\t183\t3.000000\t2006.000000\t0.000000\t0.000000\t0.000000\t0.000000\t0.000000\t1\n"+
    str(count+3) + "\t0\t3\t183\t4.000000\t950.000000\t0.000000\t0.000000\t0.000000\t0.000000\t0.000000\t1\n")
    write.close()

makeWpFile('mission.waypoints', waypoints)