import cv2
import numpy as np
import encoder as enc
import socket
import threading
            #0                 1                  2               3               4              5
dataIDS = [ 'status_request', 'status_response', 'data_request', 'data_recieve', 'instruction', 'image' ] 
port = 16253
class dataconnection:
    ip = ""
    s = "" # "" is temporary
    conn, addr = "", "" # "" is temporary until ""
    toContinue = True
    imgQueue = []

    def  __init__( self, q, theip = "127.0.0.1" ):
        ip = theip
        imgQueue = q
        s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        s.bind( ( theip, port ) )
        s.listen()
        conn, addr = s.accept()
        x = threading.Thread( target = acceptor, args=(1,))
        x.start

    def acceptor( self ):
        while toContinue:
            data = conn.recv( port )
            if not data:    # way of terminating the program from the server side, send ""
                stop()
            type = enc.getType( data )
            if type == 0:
                conn.sendall( "1" + str( len( imgQueue ) ) )
                continue
            if type == 5:
                _, img = enc.decode
                imgQueue.append( img )
    def stop( self ):
        toContinue = False