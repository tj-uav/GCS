import cv2
import numpy as np
import pickle
# first char represents base64 encoded ID of datatype, 
def getType( socketstr ):   # returns type of data stored
    section = socketstr[0]
    print( section )
    return int( section )

def decodeStatus( socketstr ):    # these couple probably don't need to be implemented
    pass                                # these communications are a bit one sided, after all
def encodeStatus( imgInQueue ):
    pass
def decodeDataReq( socketstr ):
    pass
def encodeDataReq( ImageID ):
    pass
def decodeInstruc( socketstr ):
    pass
def encodeInstruc( instruct ):
    pass
def decodeimg( socketstr ): # ImageID, Image. [1:15] represent ImageID
    bytedata = socketstr[16:]
    return int(socketstr[1:16]), decode_img(bytedata)
def encodeimg( ImageID, imgtocode ):
    bytedata = str( encode_img( imgtocode ) )
    fID = str( ImageID )
    while len(fID) < 15:
        fID = "0" + fID
    return bytes( "5" + fID + bytedata, 'utf-8' )
def encode_img(img):
        _, encoded = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 80])
        encoded = pickle.dumps(encoded)
        encoded_b64 = base64.encodebytes(encoded)
        encoded_str = encoded_b64.decode('ascii')
        return encoded_str
def decode_img( data):
    encoded_b64 = data.encode('ascii')
    encoded = base64.decodebytes(encoded_b64)
    img = pickle.loads(encoded)
    img = cv2.imdecode(img, 1)
    return img