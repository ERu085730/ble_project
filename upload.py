import time
import requests
import datetime

#upload to clouds function
def upload(temp,user):
 data =[]
 today = datetime.datetime.now() 
 s="command=insert into temperature(temp,user,minute,hour) value ("+str(temp)+","+str(user)+","+str(today.minute)+","+str(today.hour)+")"
 for t in s :
     d=ord(t)
     data.append(d)
 command=bytes(data)
 headers = {'Content-type': 'application/x-www-form-urlencoded'}
 r = requests.post('http://210.240.236.166:8079/EE122_student/test1.php?apicall=all',data=command,headers = headers)
 if r.status_code == 200:
     print('Connection Successful')
