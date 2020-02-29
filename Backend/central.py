import cv2
import numpy as np
import time
from datatransfercentral import dataconnectioncentral as DC
import threading

class datatransfercentral:  
    toContinue = True
    odclconnections = ""
    imgQueue = []
    imgProcWait = False
    x = ""
    def __init__( self, odclIPs = [ "127.0.0.1" ] ):
        #print( "WARNING: THEADING SHOULD BE IMPLEMENTED FOR FULL FUNCTIONALITY" )
        self.toContinue = True

        self.odclconnections = []
        for ip in odclIPs:
            self.odclconnections.append( DC( ip ) )
        self.x = threading.Thread( target = self.processQueue, args=())
        self.x.start()
        time.sleep( .25 )

    def processQueue( self ):   # makes a new thread and sends in background
        while self.toContinue:
            if len( self.imgQueue ) < 1:
                time.sleep( .25 )
            while len( self.imgQueue ) > 0:
                statuses = []
                for connection in self.odclconnections:
                    statuses.append( connection.getStatus() )
                self.odclconnections[ statuses.index( min( statuses ) ) ].processIMG( self.imgQueue[ 0 ] )
    def addImage( self, img ):
        self.imgQueue.append( img )
    def complete( self ): # safe program kill
        self.toContinue = False;
        self.x.join()