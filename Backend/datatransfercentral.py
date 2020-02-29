import cv2
import numpy as np
import encoder as enc
import socket
            #0                 1                  2               3               4              5
dataIDS = [ 'status_request', 'status_response', 'data_request', 'data_recieve', 'instruction', 'image' ] 
port = 16253
class dataconnectioncentral:
    ip = ""
    s = "" # "" is temporary

    def  __init__( self, theip = "127.0.0.1" ):
        ip = theip
        self.s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.s.connect( ( ip, port ) )

    def getStatus( self ):    # rets number of images in queue, 0 if empty, etc 
        self.s.sendall( "0".encode( 'utf-8' ) )
        return self.s.recv( port )
    def processIMG( self, image ):
        self.s.sendall( enc.encodeimg( ImageID = 0, imgtocode = image ) )