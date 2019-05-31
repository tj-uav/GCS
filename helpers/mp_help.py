# from geopy.distance import vincenty
import geopy
import geopy.distance
cs = None

#Radius assumes feet
def circleToPoints(centerx, centery, radius, num_points=40):
    global POINT_RADIUS
    POINT_RADIUS = 15
    CONSTANT = 0.62137119  # Miles to kilometers

    start = geopy.Point(centerx, centery)
    radius_km = (radius/5280)/CONSTANT
    dist = geopy.distance.geodesic(kilometers=radius_km)
    circlePoints = []

    for i in range(num_points):
        bearing_interval = int(360/num_points)
        new_coord = str(dist.destination(point=start, bearing=bearing_interval*i))
        new_coord = new_coord.split(", ")
        # print(new_coord)

        first = new_coord[0].split(" ")  # North/south
        north_south = float(first[0]) + (float(first[1][0:len(first[1])-1]))/60 + \
            (float(first[2][0:len(first[2])-1]))/3600
        
        if first[len(first)-1].strip() == "S":
            north_south *= -1

        second = new_coord[1].split(" ")
        east_west = float(second[0]) + (float(second[1][0:len(second[1])-1]))/60 + \
            (float(second[2][0:len(second[2])-1]))/3600

        if second[len(first)-1].strip() == "W":
            east_west *= -1

        final_coords = [north_south, east_west]
        circlePoints.append(final_coords)
    return circlePoints

def KmlBeginning():
    return """<?xml version="1.0" encoding="utf-8" ?>
    <kml xmlns="http://www.opengis.net/kml/2.2">
    <Document id="root_doc">
    <Folder><name>test</name>
    <Placemark>
	<name>polygon1</name>
	<Style><LineStyle><color>ffffffff</color></LineStyle><PolyStyle><fill>1</fill></PolyStyle></Style>
    <MultiGeometry>
    """

def KmlEnding():
    return """
    </MultiGeometry>
    </Placemark>
    </Folder>
    </Document>
    </kml>
    """

def KmlPolygon(points):
    string = """
    <Polygon>
    <outerBoundaryIs><LinearRing><coordinates>
    """
    for point in points:
        [a,b] = point
        string += str(b) + "," + str(a) + "\n"
    string += """
    </coordinates></LinearRing></outerBoundaryIs>
    </Polygon>
    """
    return string

def makeKmlFile(filename, points=[], obstacles=[], zones=[]):
    KMLSTRING = ""
    KMLSTRING += KmlBeginning()
    for point in points:
        toAdd = circleToPoints(point[0], point[1], POINT_RADIUS)
        KMLSTRING += KmlPolygon(toAdd)
    for obstacle in obstacles:
        toAdd = circleToPoints(obstacle[0], obstacle[1], obstacle[2])
        KMLSTRING += KmlPolygon(toAdd)
    for zone in zones:
        KMLSTRING += KmlPolygon(zone)
    KMLSTRING += KmlEnding()
    with open(filename, 'w+') as file:
        file.write(KMLSTRING)
        file.close()

def testMethod():
    obstacles = [[38.861164455523,-77.4728393554688,500]]
    zoneString = "-77.4471759796143,38.8609639542521 -77.4385070800781,38.8588252388515 -77.4397945404053,38.8502697340142 -77.4490642547607,38.8519408119263"
    zoneStringPoints = zoneString.split(" ")
    zones = [[[float((z.split(",")[1])), float((z.split(",")[0]))] for z in zoneStringPoints]]
    makeKmlFile('testing.kml', obstacles=obstacles, zones=zones)

if __name__ == "__main__":
    testMethod()
    # print(circleToPoints(centerx=38.8781548838115, centery=-77.3764300346375, radius = 200))
