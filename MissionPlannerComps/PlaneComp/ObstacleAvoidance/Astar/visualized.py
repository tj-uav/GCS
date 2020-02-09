import matplotlib.pyplot as plt
import time

fig, ax = plt.subplots()
ax.set_aspect(1)
plt.ylim(-300, 300)
plt.xlim(-300, 300)

# return matplotlib friendly shape
def plottable(obs):
    return plt.Circle((obs.x, obs.y), obs.r)

def tempPlot(node):
#    print("Plotting: ", node.f)
    arrX, arrY = [], []

    while node:
        arrX.append(node.x)
        arrY.append(node.y)
        node = node.parent

    arrX,arrY = arrX[::-1], arrY[::-1]
    path = plt.plot(arrX, arrY, 'bo', label="Path")[0]
#    fig.canvas.draw()
    plt.pause(0.005)
    path.remove()

def display(path, waypoints, obstacles, show=True):
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
        ax.add_artist(plottable(obs))

    plt.plot(path_x, path_y, 'ro', label='Waypoints')
    plt.plot(waypoint_x, waypoint_y, 'yo', label='Waypoints')
    plt.legend()
    if show:
        plt.show()
