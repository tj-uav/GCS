import requests
import json
import os

MISSION_ID = 1

url = "http://localhost:8000/api/"
username = "testuser"
password = "testpass"

def connect_interop(interop_url, username, password):
    r = requests.post(interop_url + "/api/login", json={"username":username, "password":password}, headers={"Content-Type":"application/json"})
    cookie_str = r.headers["Set-Cookie"].split(';')
    return cookie_str

session = requests.Session()
session.mount('http://', requests.adapters.HTTPAdapter(pool_maxsize=128, max_retries=10))
session.post(url + "login", json={"username":username, "password":password})
image_path = '/home/srikar/Downloads/testODLCimage.jpg'
#files = {'image': open(image_path, 'rb')}
#files = {'refImage': ('1.jpg', open(image_path, "rb").read(), 'image/jpeg')}
data = open(image_path,'rb').read()
print(type(data))
r = session.put(url="http://localhost:8000/api/odlcs/2/image", data=data)
print(r)
print(r.text)

r = session.get(url="http://localhost:8000/api/odlcs/2/image")
print(r.text)
print(r.headers)
