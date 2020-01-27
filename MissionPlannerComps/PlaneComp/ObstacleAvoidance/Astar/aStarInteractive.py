import matplotlib.pyplot as plt
#from scipy.interpolate import interp1d
import numpy
import random
import math
import functools
import heapq, time, random
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

@functools.total_ordering
class Node():
   global precision
   def __init__(self, x, y, parent, ang=0):
      self.x = x
      self.y = y
      self.parent = parent
      if parent:         
         self.angle = math.pi/2 *(-1*(parent.y<self.y)) if abs(parent.x-self.x) < 0.1 else math.atan((parent.y-self.y)/(parent.x-self.x)) 
      else:
         self.angle = ang

   def setF(self, f):
      self.f = f
   def dist(self, n):
      return ((n.x-self.x)**2 + (n.y-self.y)**2)**0.5
   def __hash__(self):
      return int(self.x*1000000)+int(self.y)
   def nbrs(self, obs):
      lst = []
      for d in [-math.pi/6, 0, math.pi/6]:
            lst.append(Node(self.x + precision*math.cos(self.angle+d), self.y + precision*math.sin(self.angle+d), self))
      sEt = set(lst)
      for o in obstacles:
         for n in lst:
            if o.inMe(n.x, n.y):
               sEt.remove(n)
         lst = list(sEt)
      return sEt      
   def __eq__(self, n):
      return self.dist(n)<precision*2
   def __lt__(self, n):
      return self.f<n.f

def tempPlot(node):
   arrX = []
   arrY = []
   while node:
      arrX.append(node.x)
      arrY.append(node.y)
      node = node.parent
   arrX,arrY = arrX[::-1], arrY[::-1]
   path = plt.plot(arrX, arrY, 'bo', label="Path")
   fig.canvas.draw()
   time.sleep(0.1)
   l = path.pop(0)
   l.remove()
   del l
def aStar():
   global x,y
   
   goal = Node(x[-1], y[-1], None)
   root = Node(x[-2], y[-2], None)
   root.angle = math.pi/2 *(-1*(goal.y<root.y)) if abs(goal.x-root.x) < 0.1 else math.atan((goal.y-root.y)/(goal.x-root.x))
   f = root.dist(goal)
   openSet = [root]
   pathx = []
   pathy = []
   x.remove(goal.x)
   y.remove(goal.y) 
   

   closedSet = set()
   while True:
      node = heapq.heappop(openSet)
      tempPlot(node)
      if node in closedSet: continue
      closedSet.add(node)
      for nbr in node.nbrs(obstacles):
         if nbr == goal:            
            while nbr.parent:
               pathx.append(nbr.x)
               pathy.append(nbr.y)
               nbr = nbr.parent
               
            x.extend(pathx[::-1])
            y.extend(pathy[::-1])
            x.append(goal.x)
            y.append(goal.y)

            return
         nbr.setF(nbr.dist(goal)-node.dist(goal)+f)
         heapq.heappush(openSet, nbr)


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
precision = 1

fig, ax = plt.subplots()
fig.set_size_inches(5,5)

obstacles = []
for i in range(int(input("Number of obstacles: "))):
   obstacles += [Obstacle(0,0,0)]

for i in range(len(obstacles)):
   obstacles[i].r = float(input("Size of obstacle {}: ".format(i)))

ind = 0
def onclick(event):
   
   global ind, x, y
   if ind<len(obstacles):   
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
plt.ylim(-10,10)
plt.xlim(-10,10)

ax.grid()
plt.plot(x, y, 'ro', label='Waypoints')
plt.legend()
plt.show()

# mpl_connect()