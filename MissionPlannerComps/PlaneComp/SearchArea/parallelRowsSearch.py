import matplotlib.pyplot as plt
import numpy as np

waypoints = []  # x, y
row_endpoints = []  # x, y

fig, ax = plt.subplots()
fig.set_size_inches(5, 5)

class EndPoint():
   def __init__(self, x, y):
      self.x = x
      self.y = y

   def __str__(self):
      return "Endpoint Position: ({}. {})".format(round(self.x,3), round(self.y,3))

   def plottable(self):
      return plt.Circle((self.x,self.y))

   def getX(self):
      return self.x

   def getY(self):
      return self.y

# find centroid of search area using formulas from https://en.wikipedia.org/wiki/Centroid#Of_a_polygon

def find_polygon_area(waypoint_list):
   sum = 0
   for i in range(len(waypoint_list) - 1):
      sum += (waypoint_list[i][0] * waypoint_list[i+1][1]) - (waypoint_list[i+1][0] * waypoint_list[i][1])
   return sum / 2

def centroid_x(waypoint_list, area):
   sum = 0
   for i in range(len(waypoint_list) - 1):
      sum += (waypoint_list[i][0] + waypoint_list[i+1][0])((waypoint_list[i][0] * waypoint_list[i+1][1]) - (waypoint_list[i+1][0] * waypoint_list[i][1]))
   return sum / (6 * area)

def centroid_y(waypoint_list, area):
   sum = 0
   for i in range(len(waypoint_list) - 1):
      sum += (waypoint_list[i][1] + waypoint_list[i+1][1])((waypoint_list[i][0] * waypoint_list[i+1][1]) - (waypoint_list[i+1][0] * waypoint_list[i][1]))
   return sum / (6 * area)

def find_major_axis(waypoint_list, centroid_x, centroid_y):
   # figure out a way to do this (apparently using PCA is one possible way)

