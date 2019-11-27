import time
import sys
import glob
from process import Predictor
from socket import *
from rfidCloud import readCloud
#from sendUnknown import Mail
import boto3
from botocore.exceptions import ClientError
import os
#servercode0
serverPort=12010
RFIDflag=0
pre = None

class server:
	def __init__(self):
		#self.predictObj = Predictor()
		global serverPort
		self.serverName="172.30.142.222"
		self.serverSocket = socket(AF_INET,SOCK_STREAM)
		#print("Server Port : ",serverPort)
		self.serverSocket.bind((self.serverName,serverPort))
		self.serverSocket.listen(1)
		#print("Server ready to receive requests..")


	def recvRFIDdata(self):
		print("Ready to receive RFID data : ")
		self.connSocket1,self.addr1 = self.serverSocket.accept()
		self.RFIDdata = self.connSocket1.recv(1024).decode()
		print("RFID  Data Rcvd : ",self.RFIDdata)
		id = self.RFIDdata[:13]
		text = self.RFIDdata[13:]
		print("ID : ",id)
		print("text : ",text)
		if len(text)==0:
			text="0" 
		self.rfidObj = readCloud(id,text)
		sentMail = self.rfidObj.send_email()
		self.connSocket1.send((str(sentMail)).encode())
		print("Sent Mail Status : ",sentMail)
		global RFIDflag
		RFIDflag =  sentMail

	def recvFrame(self):
		self.connSocket,self.addr = self.serverSocket.accept()
		self.flag = self.connSocket.recv(1024).decode()
		if self.flag=="true":
			os.system("./normal.sh")
		#print("FLAG  : ",self.flag)
		self.sendRecvdCmd()

	def sendRecvdCmd(self):
		global serverPort
		global pre
		global RFIDflag
		#self.connSocket.send("recvd".encode())
		#self.connSocket.close()
		self.predictObj = Predictor()
		self.prediction = self.predictObj.predictFace()
		#print("Flag Send : recvd:"+str(self.prediction))
		self.connSocket.send(("recvd:"+str(self.prediction)).encode())
		#self.deleteFrame()
		if self.prediction!=None and self.prediction!=13:
			#serverPort=11999
			#print("ServerPort after sasas:",serverPort)
			pre=self.prediction
			#self.connSocket.close()
			#self.serverSocket.close()
			#sys.exit()
			RFIDflag=0

		self.deleteFrame()

	def deleteFrame(self):
		imagepaths = glob.glob("*.jpg")
		for image in imagepaths:
			os.remove(image)

def main():
	global serverPort
	while True:
		obj = server()

		if RFIDflag==1:
			obj.recvFrame()
		if RFIDflag==0:
			obj.recvRFIDdata()

		serverPort = serverPort + 1
		#print("ServerPort2 : ",serverPort)
		time.sleep(4)

main()
