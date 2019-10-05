from auvsi_suas.client import client
from google.protobuf import json_format
import socket

ADDRESS = '192.168.86.135'
PORT = 5012

def init():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ADDRESS, PORT))
    print("Connection established.")

def main():
    cl = client.Client(url='192.168.86.138', username='testuser', password='testpass')
    mission = cl.get_mission(1)
    print("Mission: \n", mission, "\n Type: ", type(mission))
    mission = json_format.MessageToJson(mission)
    print("Mission type after conversion: ", type(mission))
    sock.send(mission.encode('utf-8'))

if __name__ == "__main__":
    init()
    main()
