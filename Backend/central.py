import cv2
import numpy as np
import time
from datatransfercentral import dataconnectioncentral as DC
import threading

class datatransfercentral:  
    toContinue = True
    odclconnections = []
    imgQueue = []
    imgProcWait = False
    def __init__( self, odclIPs = [ "127.0.0.1" ] ):
        #print( "WARNING: THEADING SHOULD BE IMPLEMENTED FOR FULL FUNCTIONALITY" )
        toContinue = True

        odclconnections = []
        for ip in odclIPs:
            val = DC( ip )
        
        x = threading.Thread( target = processQueue, args=(1,))
        x.start

    def processQueue( self ):   # makes a new thread and sends in background
        while toContinue:
            if len( imgQueue ) < 1:
                time.sleep( .25 )
            while len( imgQueue ) > 0:
                statuses = []
                for connection in odclconnections:
                    statuses.append( connection.getStatus() )
                odclconnections[ statuses.index( min( statuses ) ) ].processIMG( imgQueue[ 0 ] )
    def addImage( self, img ):
        imgQueue.add( img )
    def complete( self ): # safe program kill
        toContinue = False;