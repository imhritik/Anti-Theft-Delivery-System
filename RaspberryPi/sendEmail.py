import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

class Mail:
    def __init__(self,sender,receiver,password):
        self.email_user = sender
        self.email_password = password
        self.email_send = receiver
        self.subject = 'subject'
        self.msg = MIMEMultipart()
        self.msg['From'] = self.email_user
        self.msg['To'] = self.email_send
        self.msg['Subject'] = self.subject

    def sendMail(self,filename):
        body = 'Hi there, sending this email from Python!'
        self.msg.attach(MIMEText(body,'plain'))
        attachment  =open(filename,'rb')
        part = MIMEBase('application','octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',"attachment; filename= "+filename)
        self.msg.attach(part)
        text = self.msg.as_string()
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(self.email_user,self.email_password)


        server.sendmail(self.email_user,self.email_send,text)
        server.quit()
        
#obj = Mail('contacthritik@gmail.com','jating32@gmail.com','apple12orange')
#obj.sendMail('frame5.jpg')

