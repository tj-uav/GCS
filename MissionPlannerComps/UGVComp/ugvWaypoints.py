import matplotlib.pyplot as plt
import numpy as np
import random
import math
import functools
import heapq, time, random
import json

base_lat = 38.147250  # base coords from AUVSI rules
base_long = -76.426444

# waypoints + obstacle_list
waypoint_x = []
waypoint_y = []
waypoint_path_x = []
waypoint_path_y = []
obstacle_list = []


# precision is inversely related to speed
# dont set this to <0.05
precision = 30

# buffer zone around obstacles
# set this based off GPS accuracy
radius_tolerance = 35

class Obstacle():
    # obstacle at x,y with radius r
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    # for debugging
    def __str__(self):
        return "Center: ({}. {}), Radius: {}".format(round(self.x, 3), round(self.y, 3), round(self.r, 3))

    def inMe(self, x, y):
        return (y - self.y) ** 2 + (x - self.x) ** 2 < (self.r ** 2 + 0.5)

    # return matplotlib friendly shape
    def plottable(self):
        return plt.Circle((self.x, self.y), self.r)

def read_mission():
    global waypoint_x, waypoint_y, waypoint_path_x, waypoint_path_y, obstacle_list, forKML, og_waypoints
    forKML = []
    import requests
    s = requests.Session()
    url = "http://192.168.1.42:8000/api/"
    params = {"username": "testadmin", "password": "testpass"}
    id = 7

    r = s.post(url+"login", json=params)
    r = s.get(url+"missions/"+str(id))  
    mission_dict = json.loads(r.text)
    # for i in mission_dict['waypoints']:
    #     print(i)
    # exit()
    
    obstacle_index = 0
    for obstacle in mission_dict["stationaryObstacles"]:
        lat = obstacle["latitude"]
        lon = obstacle["longitude"]
        rad = obstacle["radius"] * 0.3048 + radius_tolerance  # feet to meters

        forKML += [[lat,lon,rad]]
        dx = (base_long - lon) * math.cos((base_lat + lat) * math.pi / 360) * 40000000 / 360  # horiz. dist from base
        dy = (base_lat - lat) * 40000000 / 360  # vert. distance from base (meters)

        obstacle_list += [Obstacle(dx, dy, rad)]
        #ax.add_artist(obstacle_list[obstacle_index].plottable())
        obstacle_index += 1

    waypont_id = 1
    og_waypoints = set()
    for waypoint in mission_dict["waypoints"]:
        lat = waypoint["latitude"]
        lon = waypoint["longitude"]

        waypoint_x.append(lat)
        waypoint_y.append(lon)

        og_waypoints.add((lat, lon))
        #label = ax.annotate(str(waypont_id), xy=(dx, dy + 10), fontsize=20, ha="center")
        waypont_id += 1

    waypoint_path_x = waypoint_x.copy()
    waypoint_path_y = waypoint_y.copy()

def writeFile(path):
    write = open('mission.waypoints', "w+")
    count = 0
    write.write("QGC WPL 110\n")#0\t1\t0\t16\t0\t0\t0\t38.881657\t-77.260719\t118.669998\n")

    for wp in path:
        count += 1
        write.write(str(count) + "\t0\t0\t16\t0.00000000\t0.00000000\t0.00000000\t0.00000000\t" + str(wp[0]) + "\t" + str(wp[1]) + "\t" + "100" + "\t1\n")

    # write.write(str(count+1)+"\t0\t3\t183\t2.000000\t988.000000\t0.000000\t0.000000\t0.000000\t0.000000\t0.000000\t1\n"+
    # str(count+2) + "\t0\t3\t183\t3.000000\t2006.000000\t0.000000\t0.000000\t0.000000\t0.000000\t0.000000\t1\n"+
    # str(count+3) + "\t0\t3\t183\t4.000000\t950.000000\t0.000000\t0.000000\t0.000000\t0.000000\t0.000000\t1\n")
    write.close()

from mp_help import makeKmlFile
def main():
    global waypoint_x, waypoint_y, waypoint_path_x, waypoint_path_y, obstacle_list, base_lat, base_long, forKML
    read_mission()
    final_path = []
    for i in range(len(waypoint_path_x)):
        final_path.append([waypoint_path_x[i], waypoint_path_y[i]])
    writeFile(final_path)
    makeKmlFile("ugvObstacles.kml", obstacles=forKML)
    print(final_path)

if __name__ == '__main__':
    main()