from auvsi_suas.client import client
from auvsi_suas.proto import interop_api_pb2
import cv2

ODCL_SHAPECONV = {'CIRCLE' : 1, 'SEMICRICLE' : 2, 'QUARTER_CIRCLE' : 3, 'TRIANGLE' : 4, 'SQUARE' : 5, 'RECTANGLE' : 6, 'TRAPEZOID' : 7, 'PENTAGON' : 8, 'HEXAGON' : 9, 'HEPTAGON' : 10, 'OCTAGON' : 11, 'STAR' : 12, 'CROSS' : 13}
ODCL_COLORCONV = {'WHITE' : 1, 'BLACK' : 2, 'GRAY' : 3, 'RED' : 4, 'BLUE' : 5, 'GREEN' : 6, 'YELLOW' : 7, 'PURPLE' : 8, 'BROWN' : 9, 'ORANGE' : 10}
ODCL_ORIENTATIONCONV = {'N' : 1, 'NE' : 2, 'E' : 3, 'SE' : 4, 'S' : 5, 'SW' : 6, 'W' : 7, 'NW' : 8}

MISSION_ID = 3
SAVE_FILENAME = 'submitting.jpg'

def connect_interop(interop_url, username, password):
    cl = client.AsyncClient(url=interop_url,
                       username=username,
                       password=password)
    return cl

def make_odlc_from_data(message_data):
    odlc = interop_api_pb2.Odlc()
    odlc.mission = MISSION_ID
    print(message_data)
    for key in message_data:
        print(key, message_data[key], type(message_data[key]))
    odlc.type = interop_api_pb2.Odlc.STANDARD
    if 'latitude' in message_data:
        odlc.latitude = message_data['latitude']
    if 'longitude' in message_data:
        odlc.longitude = message_data['longitude']
    if 'orientation' in message_data and message_data['orientation'] in ODCL_ORIENTATIONCONV:
        odlc.orientation = ODCL_ORIENTATIONCONV[message_data['orientation']]
    if 'shape' in message_data and message_data['shape'] in ODCL_SHAPECONV:
        odlc.shape = ODCL_SHAPECONV[message_data['shape']]
    if 'shape_color' in message_data and message_data['shape_color'] in ODCL_COLORCONV:
        odlc.shape_color = ODCL_COLORCONV[message_data['shape_color']]
    if 'alphanumeric' in message_data and isinstance(message_data['alphanumeric'], str):
        odlc.alphanumeric = message_data['alphanumeric']
    if 'alphanumeric_color' in message_data and message_data['alphanumeric_color'] in ODCL_COLORCONV:
        odlc.alphanumeric_color = ODCL_COLORCONV[message_data['alphanumeric_color']]
    return odlc

def submit_odcl(cl, img, data):
    odlc_object = make_odlc_from_data(data)
    odlc_object = cl.post_odlc(odlc_object).result()
    cv2.imwrite(SAVE_FILENAME, img)
    with open(SAVE_FILENAME, 'rb') as f:
        image_data = f.read()
        cl.post_odlc_image(odlc_object.id, image_data)

def crop(img, crop_data):
    x = crop_data['x']
    y = crop_data['y']
    w = crop_data['w']
    h = crop_data['h']
    return img[y:y+h, x:x+w]
