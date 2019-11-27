import pickle
import time
import cv2
import face_recognition
from retrieveFrame import Frame
import numpy as np
import glob
import collections
class Predictor:
    def __init__(self):
        #self.f = Frame()
        self.faceFound =False
    
    def Model(self):
        #self.f.sendFrame()
        self.imagepaths = glob.glob("*.jpg")
        self.predictions=[]
        print(len(self.imagepaths))
        try:
            with open("classifier.pkl","rb") as file:
                self.model = pickle.load(file)
        except:
            print("File not found")
    
    def IdentifyFace(self):
        self.Model()
        count =0
        for image in self.imagepaths:
            img = cv2.imread(image)
            count +=1
            if count ==20:
                break
            locations = face_recognition.face_locations(img)
            if locations:                
                encodings = face_recognition.face_encodings(img,locations)
                test = encodings[0].reshape(1,-1)
                predict = self.model.predict(test)
                self.predictions.append(predict[0])
                self.faceFound = True
    def predictFace(self):
        start = time.time()
        self.IdentifyFace()
        end = time.time()
        print("Execution Time : ",(end-start))
        #print(self.predictions)
        if self.faceFound:
            frequency = collections.Counter(self.predictions)
            prediction = list(frequency.keys())[0]
            for key in frequency.keys():
                if frequency[prediction] <= frequency[key]:
                    prediction = key
            #if frequency[prediction] >= 0.8 *len(self.predeictions):
        else:
            prediction = None

        print("Predict : ",prediction)
        return prediction
