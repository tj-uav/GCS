import sys
sys.path.append("C:/Python27/Lib")
sys.path.append("C:/Python27/Lib/site-packages")
sys.path.append("E:/Jason/UAV/interop/client")

from auvsi_suas.client import client
from auvsi_suas.proto import interop_api_pb2
import time, random, threading

def main():
    startup()
    t1 = threading.Thread(target=telem_data, daemon=True)
    t1.start()
    while True:
        time.sleep(1)

def startup():
    global client
    client = client.Client(url='http://192.168.1.109:8000',
                        username='testuser', password='testpass')
    mission = client.get_mission(1)
    print(mission)
    time.sleep(2)

def telem_data():
    count = 0
    while True:
        lat = random.uniform(-90, 90)
        long = random.uniform(-180, 180)
        alt = random.uniform(0, 500)
        hding = random.uniform(0, 360)
        telemetry = interop_api_pb2.Telemetry() 
        telemetry.latitude = lat
        telemetry.longitude = long
        telemetry.altitude = alt
        telemetry.heading = hding

        client.post_telemetry(telemetry)
        print("Sleeping for 0.1 seconds...")
        time.sleep(.1)
        if(count==5):
            print("Still sending")
            count = 0
        count += 1

if __name__=="__main__":
    main()
