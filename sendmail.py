import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# setting
send_address = 'asd951768@gmail.com'
receive_address = 'ss86262549@gmail.com'
host ='smtp.gmail.com'
user = send_address
password = 'az0857306719'

# message setting
message = MIMEMultipart()
message['Fron'] = send_address
message['To'] = receive_address
subject = 'Warning Temperature'
message['Subject'] = subject

#sendmail function
def sendmail(temp,userpeo):
 body = str(userpeo)+' The temperature is '+str(temp)+' Your Baby temperature higher than warning temperature you set' 
 message.attach(MIMEText(body,'plain'))
 try:
     deliver = smtplib.SMTP(host,587)
     deliver.ehlo()
     deliver.starttls()
    #deliver.connect(host,25)
     deliver.login(user,password)
     deliver.sendmail(send_address,receive_address,message.as_string())
     print('SendMail Success')

 except smtplib.SMTPException:
     print('SendMail Error') 

