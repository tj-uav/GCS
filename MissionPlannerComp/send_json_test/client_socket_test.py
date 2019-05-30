from auvsi_suas.client import client
from google.protobuf import json_format
import socket

ADDRESS = '192.168.137.27'

PORT = 5005

def init():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ADDRESS, PORT))

def main():
    cl = client.Client(url='http://98.169.139.31:8000', username='testuser', password='testpass')
    mission = cl.get_mission(1)
    print("Mission: \n", mission, "\n Type: ", type(mission))
    mission = json_format.MessageToJson(mission)
    print("Mission type after conversion: ", type(mission))
    sock.send(mission.encode('utf-8'))

if __name__ == "__main__":
    init()
    main()
