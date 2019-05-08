# ADD TO .zsh_profile PATH: /home/jasonc/.local/bin

import threading
import time
import socket
import json

COMMS_IP = '127.0.0.1'
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
        telem = {
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

        toSend = str(telem)
        toBytes = toSend.encode('utf-8')
        sock.send(toBytes)
        time.sleep(.1)
        print "Sleeping for 5 seconds..."
