import cv2
from interop_help import *

mission_id = 2
cl = connect_interop('http://192.168.1.43:8000', 'tjuav', '#checkforticks')
img = cv2.imread("jaychen.jpg")
img_data = {
    'latitude': 57.123456,
    'longitude': 74.155555,
    'orientation': 'N',
    'shape': 'QUARTER_CIRCLE',
    'shape_color': 'YELLOW',
    'alphanumeric': 'X',
    'alphanumeric_color': 'WHITE'
}

submit_odcl(cl, img, img_data)