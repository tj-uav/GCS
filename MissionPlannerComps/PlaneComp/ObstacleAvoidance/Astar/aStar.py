import matplotlib.pyplot as plt
import numpy as np
import random
import math
import functools
import heapq, time, random
import json
from mp_help import makeKmlFile

base_lat = 38.147250  # base coords from AUVSI rules
base_long = -76.426444

# waypoints + obstacle_list
waypoint_x = []
waypoint_y = []
waypoint_a = []
waypoint_path_x = []
waypoint_path_y = []
waypoint_path_a = []
obstacle_list = []


# precision is inversely related to speed
# dont set this to <0.05
precision = 30

# buffer zone around obstacles
# set this based off GPS accuracy
radius_tolerance = 35
height_tolerance = 10
pitch_tolerance = math.pi / 6

class Obstacle():
    # obstacle at x,y with radius r
    def __init__(self, x, y, r, a):
        self.x = x
        self.y = y
        self.r = r
        self.a = a

    # for debugging
    def __str__(self):
        return "Center: ({}, {}), Radius: {}, Altitude: {}".format(round(self.x, 7), round(self.y, 7), round(self.r, 7), round(self.a, 7))

    def inMe(self, x, y):
        return (y - self.y) ** 2 + (x - self.x) ** 2 < (self.r ** 2 + 0.5)

    # return matplotlib friendly shape
    def plottable(self):
        return plt.Circle((self.x, self.y), self.r)


@functools.total_ordering
class Node():
    global precision
    def __init__(self, x, y, parent, ang=0):
        self.x = x
        self.y = y
        self.parent = parent 
        if ang:
            self.angle = ang
        elif parent:
            self.angle = math.pi/2 if parent.x==self.x else math.atan2((parent.y-self.y),(parent.x-self.x))
            if self.angle < 0: self.angle += 2*math.pi
            #THIS IS BUGGY. I MADE A TEMPORARY FIX BY MANUALLY ASSIGNING AN ANGLE IN 3RD LINE OF NBRS FUNCTION
        

    def setF(self, f):
        self.f = f
    def dist(self, n):
        return ((n.x-self.x)**2 + (n.y-self.y)**2)**0.5
    def __hash__(self):
        return int(self.x*1000000)+int(self.y)
    def nbrs(self, obs):
        lst = []
        for d in [-math.pi/6, 0, math.pi/6]:
            lst.append(Node(self.x + precision*math.cos(self.angle+d), self.y + precision*math.sin(self.angle+d), self,self.angle+d))
        sEt = set(lst)
        for o in obs:
            for n in lst:
                if o.inMe(n.x, n.y):
                    sEt.remove(n)
            lst = list(sEt)
        return sEt      
    def __eq__(self, n):
        return self.dist(n)<precision*2
    def __lt__(self, n):
        return self.f<n.f

def aStar(root, goal):
    global waypoint_path_x, waypoint_path_y, precision
    root.parent = None
    f = root.dist(goal)
    openSet = [root]
    pathx = []
    pathy = []
    waypoint_path_x.remove(goal.x)
    waypoint_path_y.remove(goal.y)
    closedSet = set()
    while True:
        node = heapq.heappop(openSet)
      #   print("node",(node.x,node.y), node.dist(goal))
        if node in closedSet: continue
        closedSet.add(node)
        for nbr in node.nbrs(obstacle_list):
            if nbr == goal:
                nbr.x = goal.x
                nbr.y = goal.y
                while nbr.parent:
                    if nbr.angle != nbr.parent.angle:
                        pathx.append(nbr.x)
                        pathy.append(nbr.y)
                    nbr = nbr.parent
                waypoint_path_x.extend(pathx[::-1])
                waypoint_path_y.extend(pathy[::-1])
                # waypoint_path_x[waypoint_path_x.index(root.x) + 1: waypoint_path_x.index(root.x) + 1] = pathx[::-1]
                # waypoint_path_y[waypoint_path_y.index(root.y) + 1: waypoint_path_y.index(root.y) + 1] = pathy[::-1]
                # waypoint_path_x.append(goal.x)
                # waypoint_path_y.append(goal.y)

                return
            nbr.setF(nbr.dist(goal) - node.dist(goal) + f)
            heapq.heappush(openSet, nbr)

def distance(x1, y1, x2, y2):
    return math.sqrt((y2 - y1)**2 + (x2 - x1)**2)

def intersect(x1, y1, a1, x2, y2, a2, obstacle):
    if a1 > obstacle.a and a2 > obstacle.a:
        print("First False")
        return False

    if a1 < obstacle.a or a2 < obstacle.a:
        hSlope = (a2 - a1) / distance(x1, y1, x2, y2)
        xInt1 = distance(x1, y1, obstacle.x, obstacle.y) - obstacle.r
        xInt2 = distance(x1, y1, obstacle.x, obstacle.y) + obstacle.r
        yInt1 = hSlope * xInt1 + a1
        yInt2 = hSlope * xInt2 + a1
        if yInt1 < obstacle.a or yInt2 < obstacle.a:
            inHeight = True
            print("In Height")
        else:
            print("Not In Height")
            return False
    if inHeight:
        dist = 1000
        m1, m2 = 0, 0
        if x2 - x1 == 0:
            m1 = 10**10
        else:
            m1 = (y2 - y1) / (x2 - x1)
        b1 = y1 - (m1 * x1)  # line through two waypoints (y=mx+b)
        if m1 == 0:
            m2 = -10**10
        else:
            m2 = -1 / m1
        b2 = obstacle.y - (m2 * obstacle.x)  # perp. line through center of obstacle
        x_intersect = (b2 - b1) / (m1 - m2)
        y_intersect = (m1 * x_intersect) + b1

        if math.isclose(distance(x1, y1, x_intersect, y_intersect) + distance(x_intersect, y_intersect, x2, y2), distance(x1, y1, x2, y2), abs_tol=10**-1):
            dist = distance(x_intersect, y_intersect, obstacle.x, obstacle.y)
        else:
            dist = min(distance(x1, y1, obstacle.x, obstacle.y), distance(x2, y2, obstacle.x, obstacle.y))

        # m = (y2 - y1) / (x2 - x1)
        # a = 1 + (m ** 2)
        # b = (2 * obstacle.x) - (2 * m * y1) + (2 * m * obstacle.y)
        # c = -(obstacle.r ** 2) + (obstacle.x ** 2) - (y1 ** 2) + (2 * y1 * obstacle.y) - (obstacle.y ** 2)
        # print("m: " + str(m) + ", a: " + str(a) + ", b: " + str(b) + ", c: " + str(c))

        if dist < obstacle.r:
            # inPx1 = (-b - math.sqrt((b ** 2) - (4 * a * c))) / (2 * a)
            # inPx2 = (-b + math.sqrt((b ** 2) - (4 * a * c))) / (2 * a)
            # inPy1 = (m * inPx1) + y1
            # inPy2 = (m * inPx2) + y1
            # hSlope = (a2 - a1) / distance(x1, y1, x2, y2)
            # hX1 = distance(x1, y2, inPx1, inPy1)
            # hX2 = distance(x1, y2, inPx2, inPy2)
            # if (hSlope * hX1 + a1) < obstacle.a or (hSlope * hX2 + a1) < obstacle.a:
            #     inHeight = True
            print("End True")
            return True
        else:
            print("End False")
            return False

def read_mission():
    global waypoint_x, waypoint_y, waypoint_path_x, waypoint_path_y, obstacle_list, forKML, og_waypoints
    forKML = []
    import requests
    s = requests.Session()
    url = "http://192.168.1.250:8000/api/"
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
        alt = obstacle["height"] * 0.3048 + height_tolerance

        forKML += [[lat, lon, rad]]
        dx = (base_long - lon) * math.cos((base_lat + lat) * math.pi / 360) * 40000000 / 360  # horiz. dist from base
        dy = (base_lat - lat) * 40000000 / 360  # vert. distance from base (meters)

        obstacle_list += [Obstacle(dx, dy, rad, alt)]
        #ax.add_artist(obstacle_list[obstacle_index].plottable())
        obstacle_index += 1
    for obstacle in obstacle_list:
        print(obstacle)

    waypont_id = 1
    og_waypoints = set()
    for waypoint in mission_dict["waypoints"]:
        lat = waypoint["latitude"]
        lon = waypoint["longitude"]
        alt = waypoint["altitude"] * 0.3048

        dx = (base_long - lon) * 40000000 * math.cos((base_lat + lat) * math.pi / 360) / 360
        dy = (base_lat - lat) * 40000000 / 360

        waypoint_x.append(dx)
        waypoint_y.append(dy)
        waypoint_a.append(alt)

        og_waypoints.add((dx,dy))
        #label = ax.annotate(str(waypont_id), xy=(dx, dy + 10), fontsize=20, ha="center")
        waypont_id += 1
    print(waypoint_x, waypoint_y, waypoint_a)

    waypoint_path_x = waypoint_x.copy()
    waypoint_path_y = waypoint_y.copy()
    waypoint_path_a = waypoint_a.copy()

def read_mission_file():
    global waypoint_x, waypoint_y, waypoint_path_x, waypoint_path_y, obstacle_list, forKML, og_waypoints
    waypoints = open("testWaypoints.waypoints")
    obstaclePoints = open("obstacles.txt")
    testPoints = []
    obstacles = []
    for line in waypoints:
        testPoints.append(line)
    testPoints.pop(0)
    testPoints.pop(0)
    for i in range(len(testPoints)):
        testPoints[i] = testPoints[i][testPoints[i].index("38"):].split("\t")
        testPoints[i].pop()
    waypoints.close()
    for line in obstaclePoints:
        obstacles.append(Obstacle(float(line.split()[0]), float(line.split()[1]), float(line.split()[2]) * 0.3048, float(line.split()[3]) * 0.3048))
    obstacle_list = obstacles.copy()
    for obs in obstacles:
        print(obs)
    for point in testPoints:
        waypoint_x.append(float(point[0]))
        waypoint_y.append(float(point[1]))
        waypoint_a.append(float(point[2]) * 0.3048)
    waypoint_path_x = waypoint_x.copy()
    waypoint_path_y = waypoint_y.copy()
    waypoint_path_a = waypoint_a.copy()
    print(waypoint_path_x, waypoint_path_y, waypoint_path_a)

def generate_final_path():
    for i in range(0, len(waypoint_x)):
        for o in obstacle_list:
            print("test intersect")
            if intersect(waypoint_x[i-1], waypoint_y[i-1], waypoint_a[i-1], waypoint_x[i], waypoint_y[i], waypoint_a[i], o):
                goal = Node(waypoint_x[i], waypoint_y[i], None)
                root = Node(waypoint_x[i-1], waypoint_y[i-1], goal)
                aStar(root, goal)
                # break
    slope = lambda a,b:1000 if waypoint_path_x[a]==waypoint_path_x[b] else (waypoint_path_y[b]-waypoint_path_y[a])/(waypoint_path_x[b]-waypoint_path_x[a])
    while i+2<len(waypoint_path_x):
        if slope(i,i+1) == slope(i+1,i+2):
            del waypoint_path_x[i+1]
            del waypoint_path_y[i+1]
            i -= 1
        i += 1
    final_path = []
    print(waypoint_path_x, waypoint_path_y, waypoint_path_a)
    for coordinate in zip(waypoint_path_x, waypoint_path_y, waypoint_path_a):
        reversed_lat = -(coordinate[1] * 360 / 40000000 - base_lat)
        reversed_lon = -(coordinate[0] * 360 / 40000000 / math.cos((base_lat + reversed_lat) * math.pi / 360) - base_long)
        alt = coordinate[2]

        final_path.append((reversed_lat, reversed_lon), alt)
    return final_path

def writeFile(path):
    write = open('mission.waypoints', "w+")
    count = 0
    write.write("QGC WPL 110\n")#0\t1\t0\t16\t0\t0\t0\t38.881657\t-77.260719\t118.669998\n")

    for wp in path:
        count += 1
        write.write(str(count) + "\t0\t0\t16\t0.00000000\t0.00000000\t0.00000000\t0.00000000\t" + str(wp[0][0]) + "\t" + str(wp[0][1]) + "\t" + waypoint_path_a + "\t1\n")

    # write.write(str(count+1)+"\t0\t3\t183\t2.000000\t988.000000\t0.000000\t0.000000\t0.000000\t0.000000\t0.000000\t1\n"+
    # str(count+2) + "\t0\t3\t183\t3.000000\t2006.000000\t0.000000\t0.000000\t0.000000\t0.000000\t0.000000\t1\n"+
    # str(count+3) + "\t0\t3\t183\t4.000000\t950.000000\t0.000000\t0.000000\t0.000000\t0.000000\t0.000000\t1\n")
    write.close()

def main():
    global waypoint_x, waypoint_y, waypoint_a, waypoint_path_x, waypoint_path_y, waypoint_path_a, obstacle_list, base_lat, base_long, forKML
    # read_mission()
    read_mission_file()
    final_path = generate_final_path()
    writeFile(final_path)
    # makeKmlFile("planeObstacles.kml", obstacles=forKML)
    print(final_path)
    #display()
if __name__ == '__main__':
    main()