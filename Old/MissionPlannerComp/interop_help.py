#Gets mission object with given IP, username, password, and mission ID
def getMissionObj(ip, user, pas, id):
    import sys
    try:
        from auvsi_suas.proto import interop_api_pb2
        from auvsi_suas.client import client
    except:
        print("You didn't install AUVSI packages!")
        print("https://github.com/auvsi-suas/interop")
        sys.exit(0)    
    cl = client.AsyncClient(ip, user, pas)
    return cl.get_mission(id).result()

#Return necessary parameters to make .KML files and .waypoints files
#Uses a mission object supplied by interop client
def processMission(missionObj):
    fly_zone_data = mission_obj.fly_zones[0]
    fence_pts = []
    for pt in fly_zone_data.boundary_points:
        fence_pts.append((pt.latitude,pt.longitude))
    maxAlt = fly_zone_data.altitude_max
    minAlt = fly_zone_data.altitude_min

    grid_pts = []
    for pt in mission_obj.search_grid_points:
        grid_pts.append((pt.latitude, pt.longitude))

    waypoints = mission_obj.waypoints
    for pt in mission_obj.waypoints:
        waypoints.append((pt.latitude, pt.longitude, pt.altitude))

    obstacles_data = mission_obj.stationary_obstacles
    obstacles = []
    for obs in obstacles_data:
        obstacles.append((obs.latitude, obs.longitude, obs.radius))

    airDropPos_data = mission_obj.air_drop_pos
    airDropPos = (airDropPos_data.latitude, airDropPos_data.longitude)
    offAxisPos_data = mission_obj.off_axis_odlc_pos
    offAxisPos = (offAxisPos_data.latitude, offAxisPos_data.longitude)
    emergentPos_data = mission_obj.emergent_last_known_pos
    emergentPos = (emergentPos_data.latitude, emergentPos_data.longitude)

    points_to_draw = [airDropPos, offAxisPos, emergentPos]
    zones = [grid_pts, fence_pts]

    return points_to_draw, obstacles, zones, waypoints