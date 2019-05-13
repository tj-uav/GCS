# ADD TO .zsh_profile PATH: /home/jasonc/.local/bin

import threading
import time
import socket
import json

MESSAGE_QUEUE = deque([]) # Format for this should be dictionary
IPS = {"COMMS_COMP":'127.0.0.1', "MISSION_PLANNER":'127.0.0.1', "JETSON": '127.0.0.1', "MANUAL_DETECTION": '127.0.0.1', "MANUAL_CLASSIFICATION": '127.0.0.1'} #Change to actual values
MY_IP = IPS["MISSION_PLANNER"]
PORT = 5005

def start():
    connect_comms()
    pass

def connect_comms():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Over Internet, TCP protocol
    sock.connect((COMMS_IP, PORT)) 

    telemetry_thread = therading.Thread(target=send_telemetry)
    telemetry_thread.start()

def send_telemetry():
    print "Starting."
    while True:
        telem_full = {
        'roll': cs.roll,
        'pitch': cs.pitch,
        'yaw': cs.yaw,
        'lat': cs.lat,
        'lon': cs.lng,
        'alt': cs.alt,
        'airspeed': cs.airspeed,
        'ground_speed': cs.groundspeed,
        'vertical_speed': cs.verticalspeed,
        'wind_dir': cs.wind_dir,
        'wind_vel': cs.wind_vel,
        'acc': (cs.ax, cs.ay, cs.az),
        'gyr': (cs.gx, cs.gy, cs.gz),
        'flying_mode': cs.mode,
        'battery_voltage': cs.battery_voltage,
        'battery_remaining': cs.battery_remaining
        }

        telem_data = {
                "latitude": cs.lat,
                "longitude": cs.lng,
                "altitude": cs.alt,
                "heading": cs.wind_dir
        }

        enqueue(destination=IPS['COMMS_COMP'], header='TELEMETRY_DATA', message=telem_data)
        time.sleep(.1)
        print "Sleeping for 5 seconds..."

def enqueue(destination, header, message, subheader = None):
#    print(message)
    to_send = {}
    to_send['SOURCE'] = MY_IP
    to_send['DESTINATION'] = destination
    to_send['HEADER'] = header
    to_send['MESSAGE'] = message
    if subheader:
        to_send['SUBHEADER'] = subheader
    MESSAGE_QUEUE.append(to_send)


