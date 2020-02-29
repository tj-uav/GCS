import cv2
from central import datatransfercentral as DTC

img = cv2.imread( "a.png" )
d = DTC()
d.addImage( img )