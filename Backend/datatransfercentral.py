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

    def  __init__( self, theip ):
        ip = theip
        s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        s.connect( ( ip, port ) )

    def getStatus( self ):    # rets number of images in queue, 0 if empty, etc 
        s.sendall( "0" )
        return s.recv( port )
    def processIMG( self, image ):
        s.sendall( enc.encodeimg( 0, image ) )