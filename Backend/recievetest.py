import cv2
import time
from datatransfer import dataconnection as DC

imgs = []
c = DC( imgs )

while len( imgs ) == 0:
    time.sleep( .25 )

cv2.imwrite( imgs[0], "b.png" )
print( "saved" )