from socket import *
from subprocess import Popen
import RPi.GPIO as GPIO
import os
import time
from retrieveFrame import Frame
from readRFID import  RFID
from ultrasonic_sensor import Ultrasonic
from solenoid import Solenoid
from sendEmail import Mail
import boto3
from mfrc522 import SimpleMFRC522
from botocore.exceptions import ClientError

rfidFlag = 0
doorFlag = 0

solenoidObject = Solenoid()

try:
    file = open("portNumber.txt","r")
    serverPort = int(file.read())
    file.close()
except:
    print("File not found")

pre = None
rfidID = None
rfidText = None

class Client:
    def __init__(self):
        global serverPort
        self.serverName = "172.30.142.222"
        self.clientSocket =  socket(AF_INET,SOCK_STREAM)
        self.clientSocket.connect((self.serverName,serverPort))
        self.ultrasonicObject = Ultrasonic()
        #self.solenoidObject = Solenoid()
        #self.sentence="abc"
        #self.clientSocket.send(self.sentence.encode())

    def sendRfidData(self):
        global serverPort
        global rfidID
        global rfidText
        #print("Port: ",serverPort)        
        self.rfidObject = RFID()
        rfidData = self.rfidObject.read()
        self.id = rfidData[0]
        self.text = rfidData[1]
        rfidID = self.id
        print(rfidID)
        combinedData = str(self.id)+str(self.text)
        rfidText = combinedData[13:]
        print(rfidText)
        self.clientSocket.send(combinedData.encode())
        self.receiveRfidFlag()

    def receiveRfidFlag(self):
       self.rfidFlag = self.clientSocket.recv(1024).decode()
       global rfidFlag
       global doorFlag
       global solenoidObject
       if self.rfidFlag is not None:
           rfidFlag = int(self.rfidFlag)
           print("return flag" ,rfidFlag)
       else:
           prin
           t("recvd : " ,self.rfidFlag)
       if rfidFlag == 1 and doorFlag == 0:
           solenoidObject.unlock()
           solenoidObject.lock()
           doorFlag=1

    def callFrame(self):
        if self.ultrasonicObject.ultra():
            frame = Frame()
            frame.sendFrame()
            return True
        return False

    def start(self):
        self.sentence = "true"
        self.clientSocket.send(self.sentence.encode())
        print("STart.....")
        self.HTTPServer = Popen(["python","-m","SimpleHTTPServer","8003"])

    def end(self):
        print("End....")
        self.recv()
        if self.flag=="recvd":
            self.HTTPServer.kill()
            print("Prediction : ",self.prediction)

    def recv(self):
        global pre
        self.string = self.clientSocket.recv(1024).decode()
        #print(self.string)
        predict = self.string
        self.flag = self.string[:5]
        self.prediction = predict[6:]
        pre = self.prediction
        
    def receiverMail(self):
        global rfidID
        global rfidText
        self.dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        table = self.dynamodb.Table('Customer_1')

        response = table.scan()
        data = response['Items']

        orderid = int(rfidText)
        rfid = int(rfidID)
                
        for dic in data:
            if rfid == dic["rfID"] and orderid == dic["orderID"] :
                print("Nice")
                SENDER = "adityak1277@gmail.com"
                RECIPIENT = str(dic["Email"])
                return RECIPIENT
                
            else:
                return None
                
        


def main():
    global serverPort
    global solenoidObject
    while True:
        obj =Client()
        if rfidFlag ==0:
            print("Show rfid")
            obj.sendRfidData()
        else:
            if obj.callFrame():
                obj.start()
                obj.end()
                print(pre)
                if pre =="13":
                    print("unknown")
                    receiver = obj.receiverMail()
                    sendEmailObject = Mail('contacthritik@gmail.com',receiver,'apple12orange')
                    sendEmailObject.sendMail('frame5.jpg')
                    print("sentEmail")
                elif (pre =="0" or pre=="1" or pre =="2") and (doorFlag == 1):
                    solenoidObject.unlock()
                    solenoidObject.lock()
                    break        
                
        serverPort +=1
        try :
            file = open("portNumber.txt","w")
            file.write(str(serverPort))
            file.close()
        except:
            print("Closing ...... Not found")
           
        time.sleep(4)


main()