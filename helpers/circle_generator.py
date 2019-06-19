# from geopy.distance import vincenty
import geopy
import geopy.distance

coord = [38.8781548838115, -77.3764300346375]
radius = 200  # Asssuming feet
num_points = 10

CONSTANT = 0.62137119  # Miles to kilometers

def generate_circle(obstacle):
    
    start = geopy.Point(coord[0], coord[1])
    km = (radius/5280)/CONSTANT
    dist = geopy.distance.geodesic(kilometers=km)

    for i in range(num_points):
        bearing_interval = int(360/num_points)
        new_coord = str(dist.destination(point=start, bearing=bearing_interval*i))
        new_coord = new_coord.split(", ")
        # print(new_coord)

        first = new_coord[0].split(" ")  # North/south
        north_south = float(first[0]) + (float(first[1][0:len(first[1])-1]))/60 + \
            (float(first[2][0:len(first[2])-1]))/3600

        second = new_coord[1].split(" ")
        east_west = float(second[0]) + (float(second[1][0:len(second[1])-1]))/60 + \
            (float(second[2][0:len(second[2])-1]))/3600

        final_coord = [north_south, east_west]
        print(final_coord)
