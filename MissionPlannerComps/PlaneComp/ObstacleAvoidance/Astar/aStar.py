import matplotlib.pyplot as plt
import numpy as np
import random
import math
from math import pi, sin, cos
import functools
import heapq, time, random
import json

from mp_help import make_kml_file

fig, ax = plt.subplots()
ax.set_aspect(1)

# base_lat = 38.147250  # base coords from AUVSI rules
# base_lon = -76.426444

base_lat = 38.8355249
base_lon = -77.505455

# waypoints + obstacle_list
waypoint_x = []
waypoint_y = []
waypoint_z = []
waypoint_path_x = []
waypoint_path_y = []
waypoint_path_z = []

# constants in METERS
# precision is inversely related to speed of algorithm
# dont set this to <0.05
rho = 30

# buffer zone around obstacles
# set this based off GPS accuracy
radius_tolerance = 35
height_tolerance = 10

dPhi = pi / 12
dTheta = pi / 6
MIN_PHI = 0
MAX_PHI = pi


class Obstacle():
    # obstacle at x,y with radius r
    def __init__(self, x, y, z, r):
        self.x, self.y, self.z, self.r = x, y, z, r

    # for debugging
    def __str__(self):
        return "Center: ({}. {}), Radius: {}".format(round(self.x, 3), round(self.y, 3), round(self.r, 3))

    def inMe(self, x, y, z):
        return (y - self.y) ** 2 + (x - self.x) ** 2 < ((self.r + radius_tolerance) ** 2) and z < (self.z + height_tolerance)

    # return matplotlib friendly shape
    def plottable(self):
        return plt.Circle((self.x, self.y), self.r)


@functools.total_ordering
class Node():
    def __init__(self, x, y, z, parent=None, theta=0, phi=pi / 2):
        self.x, self.y, self.z = x, y, z
        self.parent = parent
        self.phi = phi
        self.theta = theta

    def setF(self, f):
        self.f = f

    def dist(self, n):
        return ((n.x - self.x) ** 2 + (n.y - self.y) ** 2 + (n.z - self.z) ** 2) ** 0.5

    def loc(self):
        return [self.x, self.y, self.z]

    def __hash__(self):
        return int(self.x * 1000000) + int(self.y)

    def __str__(self):
        return str(self.x) + ", " + str(self.y) + ", " + str(self.z)

    def check_collision(self, node, obs):
        for o in obs:
            if o.inMe(node.x, node.y, node.z):
                return True
        return False

    def nbrs(self, obs):
        global dPhi, dTheta
        poss = set()
#        for dp in np.arange(-pi / 12, pi / 12 + dPhi, dPhi):
#            if self.phi + dp > MAX_PHI or self.phi + dp < MIN_PHI: continue
        if True:
            dp = 0
            for dt in np.arange(-pi / 6, pi / 6 + dTheta, dTheta):
                node = Node(self.x + rho * cos(self.theta + dt) * sin(self.phi + dp),
                                self.y + rho * sin(self.theta + dt) * sin(self.phi + dp),
                                self.z + rho * cos(self.phi + dp), self, self.theta + dt, self.phi + dp)
                if not self.check_collision(node, obs):
                    poss.add(node)

        return poss

    def __eq__(self, n):
        return self.dist(n) < rho

    def __lt__(self, n):
        return self.f < n.f

def aStar(root, goal, obstacles):
    f = root.dist(goal)
    openSet = [root]
    path = []
    closedSet = set()
    num = 0
    while True:
        node = heapq.heappop(openSet)
        if node in closedSet:
            continue
        closedSet.add(node)
        for nbr in node.nbrs(obstacles):
            nbr.parent = node
            if nbr == goal:
                nbr.x = goal.x
                nbr.y = goal.y
                nbr.z = goal.z
                while nbr.parent:
                    # if nbr.theta != nbr.parent.theta or nbr.phi != nbr.parent.phi:
                    path.append(nbr.loc())
                    nbr = nbr.parent
                
                return path

            nbr.setF(nbr.dist(goal) - node.dist(goal) + f)
            heapq.heappush(openSet, nbr)
    
    return path


def read_mission():
    geo_obstacles = []
    obstacles = []
    r = open('mission.txt', 'r').read()
    mission_dict = json.loads(r)

    for obstacle in mission_dict["stationaryObstacles"]:
        lat = obstacle["latitude"]
        lon = obstacle["longitude"]
        height = obstacle["height"]
        rad = obstacle["radius"] * 0.3048  # feet to meters

        geo_obstacles.append([lat, lon, rad])
#        dx = (base_lon - lon) * cos((base_lat + lat) * pi / 360) * 40000000 / 360  # horiz. dist from base
        dx = (base_lon - lon) * 40000000 / 360
        dy = (base_lat - lat) * 40000000 / 360

        obstacles.append(Obstacle(dx, dy, height, rad))

    waypoints = []
    geo_waypoints = []
    for waypoint in mission_dict["waypoints"]:
        lat = waypoint["latitude"]
        lon = waypoint["longitude"]
        alt = waypoint["altitude"]

#        dx = (base_lon - lon) * 40000000 * cos((base_lat + lat) * pi / 360) / 360
        dx = (base_lon - lon) * 40000000 / 360
        dy = (base_lat - lat) * 40000000 / 360

        geo_waypoints.append([lat, lon, alt])
        waypoints.append([dx, dy, alt])

        if len(waypoints) > 1:
            break

    return geo_waypoints, waypoints, geo_obstacles, obstacles


def generate_final_path(waypoints, obstacles):
    paths = []
    root = Node(*waypoints[0], None)
    for i in range(1, len(waypoints)):
        goal = Node(*waypoints[i], None)
#        root = Node(*waypoints[i - 1], None)
        path = aStar(root, goal, obstacles)
        paths.append(path)
        root = path[-1]

    final_path = []
    for path in paths:
        for coordinate in path:
            final_path.append(coordinate)
#    for coordinate in waypoints:
#        reversed_lat = -(coordinate[1] * 360 / 40000000 - base_lat)
#        reversed_lon = -(coordinate[0] * 360 / 40000000 / cos((base_lat + reversed_lat) * pi / 360) - base_lon)

#        final_path.append((reversed_lat, reversed_lon, coordinate[2]))
    return final_path


def writeFile(filename, path):
    write = open(filename, "w+")
    count = 0
    write.write("QGC WPL 110\n")  # 0\t1\t0\t16\t0\t0\t0\t38.881657\t-77.260719\t118.669998\n")

    for wp in path:
        count += 1
        write.write(
            str(count) + "\t0\t0\t16\t0.00000000\t0.00000000\t0.00000000\t0.00000000\t" + str(wp[0]) + "\t" + str(
                wp[1]) + "\t" + str(wp[2]) + "\t1\n")

    write.write(
        str(count + 1) + "\t0\t3\t183\t2.000000\t988.000000\t0.000000\t0.000000\t0.000000\t0.000000\t0.000000\t1\n" +
        str(count + 2) + "\t0\t3\t183\t3.000000\t2006.000000\t0.000000\t0.000000\t0.000000\t0.000000\t0.000000\t1\n" +
        str(count + 3) + "\t0\t3\t183\t4.000000\t950.000000\t0.000000\t0.000000\t0.000000\t0.000000\t0.000000\t1\n")
    write.close()


def display(path, waypoints, obstacles):
    path_x, path_y, path_z = [], [], []
    for waypoint in path:
        path_x.append(waypoint[0])
        path_y.append(waypoint[1])
        path_z.append(waypoint[2])

    waypoint_x, waypoint_y, waypoint_z = [], [], []
    for waypoint in waypoints:
        waypoint_x.append(waypoint[0])
        waypoint_y.append(waypoint[1])
        waypoint_z.append(waypoint[2])

    print("waypoints:")
    print(path_x)
    print(path_y)

    plt.ylim(-300, 300)
    plt.xlim(-300, 300)

    ax.grid()

    for obs in obstacles:
        ax.add_artist(obs.plottable())

    plt.plot(path_x, path_y, 'ro', label='Waypoints')
    plt.plot(waypoint_x, waypoint_y, 'yo', label='Waypoints')
    plt.legend()
    plt.show()


def main():
    global waypoints, forKML
    geo_waypoints, waypoints, geo_obstacles, obstacles = read_mission()

#    writeFile("original.waypoints", og_waypoints)
    final_path = generate_final_path(waypoints, obstacles)
#    writeFile("optimized.waypoints", final_path)
#    make_kml_file("obstacles.kml", obstacles=forKML)

    # for wp in final_path:
    #     print(wp)
    # print(len(final_path), "waypoints")
    display(final_path, waypoints, obstacles)


if __name__ == '__main__':
    main()
