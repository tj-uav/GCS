import requests
import json

def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

#Temporary method
def video_capture():
    cap = cv2.VideoCapture(0)
    time.sleep(1)
    while True:
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        nparr = cv2.imencode('.jpg',frame)[1]
        temp = nparr.tolist()
        print("Numpy shape:",nparr.shape)
#        img_bytes = base64.b64decode(temp).decode('utf-8')
        img_bytes = temp
        print(type(img_bytes))
        enqueue(destination=IPS['MANUAL_DETECTION'],header='CAMERA_IMAGE',message=img_bytes)
        time.sleep(0.5)
    cap.release()
    cv2.destroyAllWindows()