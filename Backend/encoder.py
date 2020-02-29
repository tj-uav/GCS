import cv2
import numpy as np

# first char represents base64 encoded ID of datatype, 
def getType( self, socketstr ):   # returns type of data stored
    section = socketstr[0]

def decodeStatus( self, socketstr ):    # these couple probably don't need to be implemented
    pass                                # these communications are a bit one sided, after all
def encodeStatus( self, imgInQueue ):
    pass
def decodeDataReq( self, socketstr ):
    pass
def encodeDataReq( self, ImageID ):
    pass
def decodeInstruc( self, socketstr ):
    pass
def encodeInstruc( self, instruct ):
    pass
def decodeimg( self, socketstr ): # ImageID, Image. [1:15] represent ImageID
    bytedata = socketstr[16:]
    return int(socketstr[1:16]), cv2.imdecode( np.fromstring( ( bytedata ), np.uint8 ), cv2.CV_LOAD_IMAGE_COLOR )
def encodeimg( self, ImageID, imgtocode ):
    bytedata = img_str = cv2.imencode('.jpg', imgtocode)[1].tostring()
    fID = str( ImageID )
    while len(fID < 15):
        fID = " " + fID
    return "5" + fID + bytedata