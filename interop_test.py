from auvsi_suas.client import client
from auvsi_suas.proto import interop_api_pb2

# Test commit 1/18/2020

cl = client.Client(url='http://192.168.1.38:8000',
                       username='testuser',
                       password='testpass')

mission = cl.get_mission(3)
print(mission)