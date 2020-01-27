import matplotlib.pyplot as plt
# from scipy.interpolate import interp1d
import numpy
import random
import math
import functools
import heapq, time, random


class Obstacle():
    # obstacle centered at (x, y) with radius r
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    # for debugging
    def __str__(self):
        return "Center: ({}. {}), Radius: {}".format(round(self.x, 3), round(self.y, 3), round(self.r, 3))

    def contains_node(self, node):
        x = node.x
        y = node.y
        return ((y - self.y) ** 2 + (x - self.x) ** 2) < (self.r ** 2 + 0.5)

    # return matplotlib friendly shape
    def plottable(self):
        return plt.Circle((self.x, self.y), self.r)


@functools.total_ordering
class Node():
    global precision

    def __init__(self, x = None, y = None, parent):
        if x is None:
            x = random.uniform(-10, 10)
        if y is None:
            y = random.uniform(-10, 10)
        self.x = x
        self.y = y
        self.cost = 0
        self.path = []        
        self.parent = parent

    def setF(self, f):
        self.f = f
    
    def check_collision(self, obstacle_list): #Returns True if no collisions
        return all(not obstacle.contains_node(self) for obstacle in obstacle_list)

    def choose_parent(self, neighborhood):
        self.parent = get_nearest(neighborhood)
        self.cost = self.parent.cost + distance(self.parent)

    def distance(self, node):
        return (((node.x - self.x) ** 2) + ((node.y - self.y) ** 2) ** 0.5)

    def steer(self, nearest_node, step_size)
        deltaX = self.x - nearest_node.x
        deltaY = self.y - nearest_node.y
        theta = math.atan(deltaY / deltaX)
        return Node(step_size * math.cos(theta) + nearest_node.x, step_size * math.sin(theta) + nearest_node.y, nearest_node)

    def get_nearest(self, neighborhood):
        distance_list = [self.distance(node) for node in neighborhood]
        min_distance = 999
        min_index = -1
        for index, distance in enumerate(distance_list):
            if distance_list[index] < min_distance:
                min_distance = distance_list[index]
                min_index = index
        return min_index

    def get_neighborhood(self, node_list):
        radius = 10
        return [node for node in node_list if distance(node) <= radius]

    def rewire(self, neighborhood):
        for node in neighborhood:


    def __hash__(self):
        return int(self.x * 1000000) + int(self.y)


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

def rrtStar():
    global x, y, precision
    root = Node(x[-2], y[-2], None)
    goal = Node(x[-1], y[-1], None)
    node_list = [root]

    for i in range(num_waypoints):
        rand = Node()
        nearest = rand.get_nearest(node_list)
        new_node = rand.steer(nearest, precision)
        if check_collision(new_node, obstacles):
            neighborhood = new_node.get_neighborhood(node_list)
            new_node.choose_parent(node_list)
            node_list.append(new_node)

    # f = root.dist(goal)
    # openSet = [root]
    # pathx = []
    # pathy = []
    # x.remove(goal.x)
    # y.remove(goal.y)
    # closedSet = set()
    # while True:
    #     node = heapq.heappop(openSet)
    #     tempPlot(node)
    #     if node in closedSet: continue
    #     closedSet.add(node)
    #     for nbr in node.generate_neighbors(obstacles):
    #         if nbr == goal:
    #             while nbr.parent:
    #                 pathx.append(nbr.x)
    #                 pathy.append(nbr.y)
    #                 nbr = nbr.parent
    #
    #             x.extend(pathx[::-1])
    #             y.extend(pathy[::-1])
    #             x.append(goal.x)
    #             y.append(goal.y)
    #
    #             return
    #         nbr.setF(nbr.dist(goal) - node.dist(goal) + f)
    #         heapq.heappush(openSet, nbr)


def avoid():
    global x, y
    if len(x) == 1:
        x0, y0 = x[0], y[0]
        for o in obstacles:
            if o.contains_node(x0, y0):
                print("Waypoint #{} ({},{}) is inside Obstacle ({})".format(ind + 1, round(x0, 3), round(y0, 3), o))
                x.remove(x0)
                y.remove(y0)
                return
    else:
        x0, y0 = x[-2], y[-2]
        x1, y1 = x[-1], y[-1]
        rounded = [round(i, 3) for i in [x0, y0, x1, y1]]
        for o in obstacles:
            if o.contains_node(x1, y1):
                print("Waypoint #{} ({},{}) is inside Obstacle ({})".format(ind + 1, *rounded[:2], o))
                x.remove(x1)
                y.remove(y1)
                break
        aStar()


# waypoints
x = []
y = []

# precision is inversely related to speed
# dont set this to <0.05
precision = 1
num_waypoints = 30

fig, ax = plt.subplots()
fig.set_size_inches(5, 5)

obstacles = []
for i in range(int(input("Number of obstacles: "))):
    obstacles += [Obstacle(0, 0, 0)]

for i in range(len(obstacles)):
    obstacles[i].r = float(input("Size of obstacle {}: ".format(i)))

ind = 0


def onclick(event):
    global ind, x, y
    if ind < len(obstacles):
        obstacles[ind].x = event.xdata
        obstacles[ind].y = event.ydata

        ax.add_artist(obstacles[ind].plottable())
        ind += 1
    else:

        x.append(event.xdata)
        y.append(event.ydata)

        avoid()
        plt.plot(x, y, 'ro')
    for i in range(len(x)):
        plt.annotate(i, (x[i], y[i]))
    plt.show()


cid = fig.canvas.mpl_connect('button_press_event', onclick)
print([o.r for o in obstacles])
plt.ylim(-10, 10)
plt.xlim(-10, 10)

ax.grid()
plt.plot(x, y, 'ro', label='Waypoints')
plt.legend()
plt.show()

# mpl_connect()
