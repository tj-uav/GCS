import time
import cv2


def video_capture():
    cap = cv2.VideoCapture(0)
    time.sleep(1)
    for x in range(100):
        ret, frame = cap.read()
        cv2.imwrite('img/'+str(x)+'.png', frame)
        time.sleep(0.1)
    cap.release()
    cv2.destroyAllWindows()

video_capture()