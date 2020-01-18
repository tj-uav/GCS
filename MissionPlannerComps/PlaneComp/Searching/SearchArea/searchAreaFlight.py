import matplotlib.pyplot as plt
from scipy.spatial.qhull import ConvexHull
import numpy as np

areaEdgePoints = []
currentLoc = []


class EdgePoint():
   def __init__(self, x, y):
      self.x = x
      self.y = y

   def __str__(self):
      return "Edge Point Position: ({}. {})".format(round(self.x,3), round(self.y,3))

   def plottable(self):
      return plt.Circle((self.x,self.y))

   def getX(self):
      return self.x

   def getY(self):
      return self.y


class PlaneLoc():
   def __init__(self, x, y):
      self.x = x
      self.y = y

   def __str__(self):
      return "Plane Position: ({}. {})".format(round(self.x, 3), round(self.y, 3))

   def plottable(self):
      return plt.plot(x, y, 'bl')

   def getX(self):
      return self.x

   def getY(self):
      return self.y


# waypoints
x = []
y = []
planeX = []
planeY = []


fig, ax = plt.subplots()
fig.set_size_inches(5, 5)

edgePoints = []
numEdgePoints = int(input("Number of EdgePoints: "))
for i in range(numEdgePoints):
   edgePoints += [EdgePoint(0, 0)]

planeLocation = PlaneLoc(0, 0)
numClick = 0
ind = 0

def onclick(event):
   global ind, x, y, numClick
   if numClick < numEdgePoints:
      x.append(event.xdata)
      y.append(event.ydata)

      plt.plot(x, y, 'ro')
      for i in range(len(x)):
         plt.plot(x[i], y[i])
      numClick += 1

      if numClick == numEdgePoints:
         points = []
         if len(x) == numEdgePoints:
            for i in range(len(x)):
               points.append(np.asarray((x[i], y[i])).reshape(1, 2))
         points = np.array(points).reshape(numEdgePoints, 2)

         hull = ConvexHull(points)
         for simplex in hull.simplices:
            plt.plot(points[simplex, 0], points[simplex, 1], '-r')
      plt.show()

   elif numClick == numEdgePoints:
      planeX.append(event.xdata)
      planeY.append(event.ydata)

      plt.plot(planeX, planeY, 'bo')
      for i in range(len(planeX)):
         plt.plot(planeX[i], planeY[i])
      numClick += 1

      minDistance = float("inf")
      pointIndex = -1
      for i in range(len(x)):
         dist = (((planeX[0] - x[i]) ** 2) + ((planeY[0] - y[i]) ** 2)) ** (1/2)
         if dist < minDistance:
            minDistance = dist
            pointIndex = i
      plt.plot([planeX[0], x[pointIndex]], [planeY[0], y[pointIndex]], 'bo-')

      theta = np.pi/4
      sinX = np.arange(0, 200, 0.1)
      sinY = []
      for val in sinX:
         sinY.append(50 * np.sin(0.1*val))

      x_prime = []
      y_prime = []
      for i in range(len(sinX)):
         x_prime.append(sinX[i] * np.cos(theta) - sinY[i] * np.sin(theta))
         y_prime.append(sinX[i] * np.sin(theta) + sinY[i] * np.cos(theta))
      plt.plot(x_prime + x[pointIndex], y_prime + y[pointIndex], 'b')

      plt.show()


cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.ylim(0, 200)
plt.xlim(0, 200)

ax.grid()
plt.plot(x, y, 'ro', label='Search Area Edge Points')
plt.plot(planeX, planeY, 'bo', label='Plane Location and Path')
plt.legend()
plt.show()