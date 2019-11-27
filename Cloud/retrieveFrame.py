import cv2
import time
import glob
import os

class Frame:
    def __init__(self):
        pass
    def removeImg(self):
        imagepaths = glob.glob("*.jpg")
        for image in imagepaths:
            os.remove(image)
    


    def sendFrame(self):
        self.removeImg()
        cap = cv2.VideoCapture(0)
        i=0
        start = time.time()

        while time.time() - start < 2 :
            i +=1
            ret,frame = cap.read()
            cv2.imshow('frame',frame)
            cv2.imwrite("frame"+str(i)+".jpg",frame)
            if cv2.waitKey(1) & 0xFF==27:
                break
        cap.release()
        cv2.destroyAllWindows()


