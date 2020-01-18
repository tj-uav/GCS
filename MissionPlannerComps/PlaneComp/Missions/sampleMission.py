from TJUAV.FC.makeWaypointFile import automission

my_mission = automission('copter')


lat, lon = 38.1446916666667, -76.4279944444445
alt = 200.0

my_mission.takeoff(angle = 10, alt = 15)

my_mission.waypoint(lat, lon, alt)

my_mission.waypoint(lat+0.001, lon-0.0002, alt+5)

my_mission.do_set_roi(38.1415777777778, -76.4252472222222)
for i in range(15):
	my_mission.waypoint(lat, lon, alt)
	my_mission.do_digicam_control()
	lat+=0.001 if i%4==0 else 0
	lon+=0.001 if i%4==1 else 0
	lat+=0.001 if i%4==2 else 0
	lon-=0.001 if i%4==3 else 0
	alt += 10

my_mission.rtl()


my_mission.write()