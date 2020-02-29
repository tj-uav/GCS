import cv2
import numpy as np
import encoder as enc
import socket
import threading
import time
            #0                 1                  2               3               4              5
dataIDS = [ 'status_request', 'status_response', 'data_request', 'data_recieve', 'instruction', 'image' ] 
port = 16253
class dataconnection:
    s = "" # "" is temporary unti __init__
    conn, addr = "", "" # "" is temporary until "" until
    toContinue = True
    imgQueue = []
    x = ""

    def  __init__( self, q ):
        self.imgQueue = q
        self.s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.s.bind( ( "127.0.0.1", port ) )
        print( "waiting..." )
        self.s.listen()
        self.conn, self.addr = self.s.accept()
        print( "connected " + str( self.addr ) )
        self.x = threading.Thread( target = self.acceptor, args=(1,))
        self.x.start
        time.sleep( .25 )

    def acceptor( self ):
        while toContinue:
            data = str( self.conn.recv( port ) )
            print( "recieved!" )
            if not data:    # way of terminating the program from the server side, send ""
                self.stop()
            type = enc.getType( data )
            if type == 0:
                self.conn.sendall( str( len( self.imgQueue ) ).encode( 'utf-8' ) )
                continue
            if type == 5:
                _, img = enc.decode
                self.imgQueue.append( img )
    def stop( self ):
        self.toContinue = False
        x.join()