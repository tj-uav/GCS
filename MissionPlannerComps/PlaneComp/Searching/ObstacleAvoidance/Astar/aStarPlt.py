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
precision = 20

# buffer zone around obstacles
# set this based off GPS accuracy
radius_tolerance = 20

fig, ax = plt.subplots()
fig.set_size_inches(15, 15)


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


@functools.total_ordering
class Node():
    global precision

    def __init__(self, x, y, parent):
        self.x = x
        self.y = y
        self.parent = parent

    def __str__(self):
        return "{}, {}".format(self.x, self.y)

    def setF(self, f):
        self.f = f

    def dist(self, n):
        return ((n.x - self.x) ** 2 + (n.y - self.y) ** 2) ** 0.5

    def __hash__(self):
        return int(self.x * 1000000) + int(self.y)

    def nbrs(self, obs, angle):
        lst = []
        for d in [-math.pi/6, 0, math.pi/6]:
            lst.append(Node(self.x + precision*math.cos(angle+d), self.y + precision*math.sin(angle+d), self))
        sEt = set(lst)
        for o in obstacle_list:
            for n in lst:
                if o.inMe(n.x, n.y):
                    sEt.remove(n)
            lst = list(sEt)
        return sEt

    def __eq__(self, n):
        return self.dist(n) < precision

    def __lt__(self, n):
        return self.f < n.f


def tempPlot(node):
    arrX = []
    arrY = []
    while node:
        arrX.append(node.x)
        arrY.append(node.y)
        node = node.parent
    arrX, arrY = arrX[::-1], arrY[::-1]
    path = plt.plot(arrX, arrY, 'bo', label="Path")
    fig.canvas.draw()
    time.sleep(0.1)
    l = path.pop(0)
    l.remove()
    del l


def aStar(root, goal):
    global waypoint_path_x, waypoint_path_y
    f = root.dist(goal)
    openSet = [root]
    pathx = []
    pathy = []
    waypoint_path_x.remove(goal.x)
    waypoint_path_y.remove(goal.y)
    closedSet = set()
    while True:
        node = heapq.heappop(openSet)
        tempPlot(node)
        if node in closedSet: continue
        closedSet.add(node)
        ang = math.pi/2 *(-1*(goal.y<root.y)) if goal.x-root.x < 0.1 else math.atan((goal.y-root.y)/(goal.x-root.x))
        for nbr in node.nbrs(obstacle_list, ang):
            if nbr == goal:
                while nbr.parent:
                    pathx.append(nbr.x)
                    pathy.append(nbr.y)
                    nbr = nbr.parent

                waypoint_path_x[waypoint_path_x.index(root.x) + 1: waypoint_path_x.index(root.x) + 1] = pathx[::-1]
                waypoint_path_y[waypoint_path_y.index(root.y) + 1: waypoint_path_y.index(root.y) + 1] = pathy[::-1]
                # waypoint_path_x.append(goal.x)
                # waypoint_path_y.append(goal.y)

                return
            nbr.setF(nbr.dist(goal) - node.dist(goal) + f)
            heapq.heappush(openSet, nbr)
    plt.show()


def distance(x1, y1, x2, y2):
    return math.sqrt((y2 - y1)**2 + (x2 - x1)**2)


def intersect(x1, y1, x2, y2, obstacle):
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

    return dist < obstacle.r

def read_mission():
    global waypoint_x, waypoint_y, waypoint_path_x, waypoint_path_y, obstacle_list, forKML, og_waypoints
    forKML = []
    import requests
    s = requests.Session()
    url = "http://192.168.1.38:8000/api/"
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

        dx = (base_long - lon) * 40000000 * math.cos((base_lat + lat) * math.pi / 360) / 360
        dy = (base_lat - lat) * 40000000 / 360

        waypoint_x.append(dx)
        waypoint_y.append(dy)

        og_waypoints.add((dx,dy))
        #label = ax.annotate(str(waypont_id), xy=(dx, dy + 10), fontsize=20, ha="center")
        waypont_id += 1

    waypoint_path_x = waypoint_x.copy()
    waypoint_path_y = waypoint_y.copy()


def generate_final_path():
    for i in range(1, len(waypoint_x)):
        # for o in obstacle_list:
        #     if intersect(waypoint_x[i-1], waypoint_y[i-1], waypoint_x[i], waypoint_y[i], o):
        aStar(Node(waypoint_x[i-1], waypoint_y[i-1], None), Node(waypoint_x[i], waypoint_y[i], None))
        print('hi')
                # break
    slope = lambda a,b:1000 if waypoint_path_x[a]==waypoint_path_x[b] else (waypoint_path_y[b]-waypoint_path_y[a])/(waypoint_path_x[b]-waypoint_path_x[a])
    while i+2<len(waypoint_path_x):
        if i<6:
            print(slope(i,i+1), slope(i+1,i+2))
        if slope(i,i+1) == slope(i+1,i+2):
            del waypoint_path_x[i+1]
            del waypoint_path_y[i+1]
            i -= 1
        i += 1
    final_path = []
    for coordinate in zip(waypoint_path_x, waypoint_path_y):
        reversed_lat = -(coordinate[1] * 360 / 40000000 - base_lat)
        reversed_lon = -(coordinate[0] * 360 / 40000000 / math.cos((base_lat + reversed_lat) * math.pi / 360) - base_long)
        
        final_path.append((reversed_lat, reversed_lon))
    return final_path


def display():
    ax.grid()
    plt.axis('equal')
    plt.plot(waypoint_path_x, waypoint_path_y, 'ro', label='Waypoints')
    boolean = True
    for i in range(1, len(waypoint_path_x)):
        for o in obstacle_list:
            if intersect(waypoint_path_x[i - 1], waypoint_path_y[i - 1], waypoint_path_x[i], waypoint_path_y[i], o):
                boolean = False
                break
        if boolean:
            plt.plot([waypoint_path_x[i - 1], waypoint_path_x[i]], [waypoint_path_y[i - 1], waypoint_path_y[i]], 'ro-')
    ax.relim()
    ax.autoscale_view()
    plt.legend()
    plt.show()
def writeFile(path):
    write = open('mission.waypoints', "w+")
    count = 0
    write.write("QGC WPL 110\n")#0\t1\t0\t16\t0\t0\t0\t38.881657\t-77.260719\t118.669998\n")

    for wp in path:
        count += 1
        write.write(str(count) + "\t0\t0\t16\t0.00000000\t0.00000000\t0.00000000\t0.00000000\t" + str(wp[0]) + "\t" + str(wp[1]) + "\t" + "100" + "\t1\n")

    write.write(str(count+1)+"\t0\t3\t183\t2.000000\t988.000000\t0.000000\t0.000000\t0.000000\t0.000000\t0.000000\t1\n"+
    str(count+2) + "\t0\t3\t183\t3.000000\t2006.000000\t0.000000\t0.000000\t0.000000\t0.000000\t0.000000\t1\n"+
    str(count+3) + "\t0\t3\t183\t4.000000\t950.000000\t0.000000\t0.000000\t0.000000\t0.000000\t0.000000\t1\n")
    write.close()
from mp_help import makeKmlFile
def main():
    global waypoint_x, waypoint_y, waypoint_path_x, waypoint_path_y, obstacle_list, base_lat, base_long, forKML
    read_mission()
    final_path = generate_final_path()
    writeFile(final_path)
    makeKmlFile("obstacles.kml", obstacles=forKML)
    print(final_path)
    #display()


if __name__ == '__main__':
    main()
