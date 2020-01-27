import matplotlib.pyplot as plt
#from scipy.interpolate import interp1d
import numpy
import random
import math
import functools
import heapq, time, random
import os

DISPLAY_SPEED = 0.5
OBSTACLE_INTERVAL = 0.2

def dist(a, b):
   (x1, y1) = a
   (x2, y2) = b
   return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


class Obstacle():
   #obstacle at x,y with radius r
   def __init__(self, x, y, r):
      self.x = x
      self.y = y
      self.r = r
   #for debugging
   def __str__(self):
      return "Center: ({}. {}), Radius: {}".format(round(self.x,3), round(self.y,3), round(self.r,3))
   def inMe(self, x, y):
      return (y-self.y)**2+(x-self.x)**2 < (self.r**2+0.5)
   #return matplotlib friendly shape
   def plottable(self):
      return plt.Circle((self.x,self.y), self.r)

class MovingObstacle(Obstacle):
   #Moving obstacle with constant radius, but changing x and y
   def __init__(self, filename):
      self.filename = filename
      self.path = []
      file = open(filename, "r")
      lines = file.readlines()
      self.r, self.speed = [float(i.strip()) for i in lines.split(",")]
      for line in lines[1:]:
         x,y = line.strip().split(",")
         self.path.append((int(x), int(y)))
      file.close()
      self.t = 0
      self.x, self.y = self.path[self.t]
   
   def __init__(self, r, speed):
      self.path = []
      self.r = r
      self.t = 0
      self.x, self.y = 0,0
      self.speed = speed
   
   def setPath(self, start, end):
      self.path = []
      distance = dist(end, start)
      num_points = distance / OBSTACLE_INTERVAL
      diffX = (end[0] - start[0]) / num_points
      diffY = (end[1] - start[1]) / num_points
      for i in range(int(num_points + 1)):
         self.path.append((start[0] + i*diffX, start[1] + i*diffY))

   def posAt(self, t):
      aX, aY = self.path[min(int(t*self.speed), len(self.path) - 1)]
      bX, bY = self.path[min(int(t*self.speed) + 1, len(self.path) - 1)]
      return (t * self.speed * (bX - aX)) + aX, (t * self.speed * (bY - aY)) + aY 

   def inMe(self, x, y, t):
      self.x, self.y = self.posAt(t)
      return (y-self.y)**2+(x-self.x)**2 < (self.r**2+0.5)

   def plottable(self, t):
      self.x, self.y = self.posAt(t)
      self.patch = plt.Circle((self.x,self.y), self.r, color='green')
      return self.patch

   def move(self, t):
      self.x, self.y = self.posAt(t)
      self.patch.center = self.x, self.y


@functools.total_ordering
class Node():

   global precision
   def __init__(self, x, y, parent):
      self.x = x
      self.y = y
      self.parent = parent

   def setF(self, f):
      self.f = f

   def dist(self, n):
      return dist((self.x, self.y), (n.x, n.y))

   def __hash__(self):
      return int(self.x*1000000)+int(self.y)

   def nbrs(self, obs, mov, t):
      lst = []
      for i in [-precision, 0, precision]:
         for j in [-precision, 0, precision]:
            lst.append(Node(self.x+i, self.y+j, self))
      sEt = set(lst)
      for o in obs:
         for n in lst:
            if o.inMe(n.x, n.y):
               sEt.remove(n)
         lst = list(sEt)

      for o in mov:
         for n in lst:
            if o.inMe(n.x, n.y, t+1):
               sEt.remove(n)
         lst = list(sEt)

      return sEt      
   def __eq__(self, n):
      return self.dist(n)<precision
   def __lt__(self, n):
      return self.f<n.f

def tempPlot(node, moving):
   arrX = []
   arrY = []
   while node:
      arrX.append(node.x)
      arrY.append(node.y)
      node = node.parent
   arrX,arrY = arrX[::-1], arrY[::-1]
   path = plt.plot(arrX, arrY, 'b', label="Path")
   movX, movY = [], []

   for obs in moving:
      obs.move(len(arrX))

#   for obs in moving:
#      pos = obs.posAt(len(arrX))
#      movX.append(pos[0])
#      movY.append(pos[1])

#   for a in range(len(movX)):
#      circle = plt.Circle((movX[a], movY[a]), moving[a].r, color='green')
#      ax.add_artist(circle)
#      path = plt.plot(movX, movY, 'go', label="Moving")
   fig.canvas.draw()
   time.sleep(0.005)
   l = path.pop(0)
   l.remove()
   del l

def aStar():
   global x,y
   root = Node(x[-2], y[-2], None)
   goal = Node(x[-1], y[-1], None)
   f = root.dist(goal)
   openSet = [(root, 0)]
   pathx = []
   pathy = []
   x.remove(goal.x)
   y.remove(goal.y)
   closedSet = set()
   while True:
      node, curr_t = heapq.heappop(openSet)
      tempPlot(node, moving)
      if node in closedSet: continue
      closedSet.add(node)
      for nbr in node.nbrs(obstacles, moving, curr_t):
         if nbr == goal:            
            while nbr.parent:
#               print(curr_t - len(pathx))
               print(dist((nbr.x, nbr.y), moving[0].posAt(curr_t - len(pathx))))
               pathx.append(nbr.x)
               pathy.append(nbr.y)
               nbr = nbr.parent
               
            x.extend(pathx[::-1])
            y.extend(pathy[::-1])
            x.append(goal.x)
            y.append(goal.y)

            return
         nbr.setF(nbr.dist(goal)-node.dist(goal)+f)
         heapq.heappush(openSet, (nbr, curr_t+1))
      time.sleep(.01/DISPLAY_SPEED)


def avoid():
   global x,y
   if len(x)==1:
      x0, y0 = x[0], y[0]
      for o in obstacles:
         if o.inMe(x0, y0):
            print("Waypoint #{} ({},{}) is inside Obstacle ({})".format(ind+1,round(x0,3), round(y0,3),o))
            x.remove(x0)
            y.remove(y0)
            return
   else:
      x0, y0 = x[-2], y[-2]
      x1, y1 = x[-1], y[-1]
      rounded = [round(i,3) for i in [x0, y0, x1, y1]]
      for o in obstacles:
         if o.inMe(x1, y1):
            print("Waypoint #{} ({},{}) is inside Obstacle ({})".format(ind+1,*rounded[:2],o))
            x.remove(x1)
            y.remove(y1)
            break
      aStar()
            
      

# waypoints
x = []
y = []

# precision is inversely related to speed
# dont set this to <0.05
PRESET_OBSTACLES = True
obstacles = []
moving = [MovingObstacle(1,3)]

precision = 1

fig, ax = plt.subplots()
fig.set_size_inches(5,5)

if not PRESET_OBSTACLES:
#   moving_filenames = ["moving1.txt"]
   obstacles = []
   moving = []
   for i in range(int(input("Number of obstacles: "))):
      obstacles.append(Obstacle(0,0,0))

   for i in range(len(obstacles)):
      obstacles[i].r = float(input("Size of obstacle {}: ".format(i)))

   for i in range(int(input("Number of moving obstacles: "))):
   #for file in moving_filenames:
      moving.append(MovingObstacle(0,0))

   for i in range(len(moving)):
      moving[i].r = float(input("Radius of obstacle {}: ".format(i)))
      moving[i].speed = float(input("Speed of obstacle {}: ".format(i)))
   #   moving.append(MovingObstacle("moving_obstacles/" + file))


ind = 0
mov_pos = (0,0)
def onclick(event):
   
   global ind, x, y, mov_pos
   if ind<len(obstacles):   
      obstacles[ind].x = event.xdata
      obstacles[ind].y = event.ydata

      ax.add_artist(obstacles[ind].plottable())
      ind += 1

   elif ind < len(obstacles) + len(moving)*2:
      if (ind - len(obstacles)) % 2 == 0:
         mov_pos = (event.xdata, event.ydata)
      else:
         moving[ind // 2].setPath(mov_pos, (event.xdata, event.ydata))
         ax.add_artist(moving[ind // 2].plottable(0))
         mov_pos = (0,0)
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
plt.ylim(-10,10)
plt.xlim(-10,10)

ax.grid()
plt.plot(x, y, 'ro', label='Waypoints')
plt.legend()
plt.show()

# mpl_connect()