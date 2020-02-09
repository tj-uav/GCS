import matplotlib.pyplot as plt
import numpy as np
import random
import math
from math import pi, sin, cos
import functools
import heapq, time, random
import json

base_lat = 38.147250  # base coords from AUVSI rules
base_long = -76.426444

# waypoints + obstacle_list
waypoint_x = []
waypoint_y = []
waypoint_z = []
waypoint_path_x = []
waypoint_path_y = []
waypoint_path_z = []
obstacle_list = []

# constants in METERS
# precision is inversely related to speed of algorithm
# dont set this to <0.05
rho = 30

# buffer zone around obstacles
# set this based off GPS accuracy
radius_tolerance = 35
height_tolerance = 10

dPhi = pi/12
dTheta = pi/6
MIN_PHI = 0
MAX_PHI = pi
class Obstacle():
   # obstacle at x,y with radius r
   def __init__(self, x, y, z, r):
      self.x = x
      self.y = y
      self.z = z
      self.r = r

   # for debugging
   def __str__(self):
      return "Center: ({}. {}), Radius: {}".format(round(self.x, 3), round(self.y, 3), round(self.r, 3))

   def inMe(self, x, y, z):
      return False#(y - self.y) ** 2 + (x - self.x) ** 2 < ((self.r+radius_tolerance) ** 2) and (self.z+height_tolerance) >=z

   # return matplotlib friendly shape
   def plottable(self):
      return plt.Circle((self.x, self.y), self.r)


@functools.total_ordering
class Node():
   def __init__(self, x, y, z, parent=None, theta=0, phi=pi/2):
      self.x, self.y, self.z = x,y,z
      self.parent = parent 
      self.phi = phi
      self.theta = theta
   def setF(self, f):
      self.f = f
   def dist(self, n):
      return ((n.x-self.x)**2 + (n.y-self.y)**2 + (n.z-self.z)**2)**0.5
   def loc(self):
      return [self.x,self.y,self.z]
   def __hash__(self):
      return int(self.x*1000000)+int(self.y)
   def nbrs(self, obs):
      global dPhi, dTheta
      lst = []
      for dp in np.arange(-pi/12, pi/12+dPhi, dPhi):
         if self.phi+dp > MAX_PHI or self.phi+dp < MIN_PHI: continue
         for dt in np.arange(-pi/6, pi/6+dTheta, dTheta):
            lst.append(Node(self.x + rho*cos(self.theta+dt)*sin(self.phi+dp), self.y + rho*sin(self.theta+dt)*sin(self.phi+dp), self.z + rho*cos(self.phi+dp), self,self.theta+dt, self.phi+dp))
      sEt = set(lst)
      for o in obs:
         for n in lst:
            if o.inMe(n.x, n.y, n.z):
               sEt.remove(n)
         lst = list(sEt)
      return sEt     
   def __eq__(self, n):
      global rho
      return self.dist(n)<rho
   def __lt__(self, n):
      return self.f<n.f

def aStar(root, goal):
   global waypoints, rho
   root.parent = None
   f = root.dist(goal)
   openSet = [root]
   path = []
   waypoints.remove(goal.loc())
   closedSet = set()
   num = 0
   while True:
      node = heapq.heappop(openSet)
      if node in closedSet: continue
      closedSet.add(node)
      for nbr in node.nbrs(obstacle_list):
         goal.parent = node
         if nbr == goal:
            nbr.x = goal.x
            nbr.y = goal.y
            nbr.z = goal.z
            while nbr.parent:
               if nbr.theta != nbr.parent.theta or nbr.phi != nbr.parent.phi:
                  path.append(nbr.loc())
               nbr = nbr.parent
            waypoints.extend(path[::-1])
            return
         nbr.setF(nbr.dist(goal) - node.dist(goal) + f)
         heapq.heappush(openSet, nbr)

def read_mission():
   global waypoints, obstacle_list, forKML
   forKML = []
   import requests
   s = requests.Session()
   url = "http://192.168.1.43:8000/api/"
   params = {"username": "testadmin", "password": "testpass"}
   id = 7

   # r = s.post(url+"login", json=params)
   # r = s.get(url+"missions/"+str(id))  
   r = open('mission.txt', 'r').read()
   mission_dict = json.loads(r)
   #mission_dict = json.loads(r.text)

   for obstacle in mission_dict["stationaryObstacles"]:
      lat = obstacle["latitude"]
      lon = obstacle["longitude"]
      height = obstacle["height"]
      rad = obstacle["radius"] * 0.3048  # feet to meters

      forKML += [[lat,lon,rad]]
      dx = (base_long - lon) * cos((base_lat + lat) * pi / 360) * 40000000 / 360  # horiz. dist from base
      dy = (base_lat - lat) * 40000000 / 360  # vert. distance from base (meters)

      obstacle_list += [Obstacle(dx, dy, height, rad)]

   waypoints = []
   og_waypoints = []
   for waypoint in mission_dict["waypoints"]:
      lat = waypoint["latitude"]
      lon = waypoint["longitude"]
      alt = waypoint["altitude"]

      dx = (base_long - lon) * 40000000 * cos((base_lat + lat) * pi / 360) / 360
      dy = (base_lat - lat) * 40000000 / 360

      og_waypoints.append([lat,lon,alt])
      waypoints.append([dx,dy,alt])

      if len(waypoints)>1: break
   return og_waypoints


def generate_final_path():
   global waypoints
   for i in range(len(waypoints)):
      goal = Node(*waypoints[i], None)
      root = Node(*waypoints[i-1], goal)
      aStar(root, goal)

   final_path = []
   for coordinate in waypoints:
      reversed_lat = -(coordinate[1] * 360 / 40000000 - base_lat)
      reversed_lon = -(coordinate[0] * 360 / 40000000 / cos((base_lat + reversed_lat) * pi / 360) - base_long)
      
      final_path.append((reversed_lat, reversed_lon, coordinate[2]))
   return final_path
def writeFile(filename, path):
   write = open(filename, "w+")
   count = 0
   write.write("QGC WPL 110\n")#0\t1\t0\t16\t0\t0\t0\t38.881657\t-77.260719\t118.669998\n")

   for wp in path:
      count += 1
      write.write(str(count) + "\t0\t0\t16\t0.00000000\t0.00000000\t0.00000000\t0.00000000\t" + str(wp[0]) + "\t" + str(wp[1]) + "\t" + str(wp[2]) + "\t1\n")

   write.write(str(count+1)+"\t0\t3\t183\t2.000000\t988.000000\t0.000000\t0.000000\t0.000000\t0.000000\t0.000000\t1\n"+
   str(count+2) + "\t0\t3\t183\t3.000000\t2006.000000\t0.000000\t0.000000\t0.000000\t0.000000\t0.000000\t1\n"+
   str(count+3) + "\t0\t3\t183\t4.000000\t950.000000\t0.000000\t0.000000\t0.000000\t0.000000\t0.000000\t1\n")
   write.close()
from mp_help import makeKmlFile
def main():
   global waypoints, forKML
   og_waypoints = read_mission()
   writeFile("original.waypoints",og_waypoints)
   final_path = generate_final_path()
   writeFile("optimized.waypoints",final_path)
   makeKmlFile("obstacles.kml", obstacles=forKML)
   for wp in final_path: print(wp)
   print(len(final_path), "waypoints")
   #display()
if __name__ == '__main__':
   main()
