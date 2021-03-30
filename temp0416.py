# coding: utf-8
from tkinter import*
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.messagebox
import time
import threading
import array
import sys
import numpy as np
import pexpect
import RPi.GPIO as GPIO
from upload import upload
from sendmail import sendmail

cn1='C0:26:DE:00:10:70' #watch mac address
cn2='C0:26:DE:00:0B:A4'

war1=30 # initial temperature  warning value
war2=30

t=0 #data x axis
tt=0 #
k=0

ty1=np.array([0]) #use in chart
tx1=np.array([0])
ty2=np.array([0])
tx2=np.array([0])

class bluetoothcn(threading.Thread):
 def __init__(self,cond):
  super(bluetoothcn,self).__init__()
  self.cond = cond
  
 def run(self): #run 2to1 ble connect
  self.cond.acquire()
  global tool ,tool1
  global tx1,ty1
  global tx2,ty2
  global t,tt
  global figure1,figure2
  
  while True:
   tool = pexpect.spawn('gatttool -t random -b ' + 'C0:26:DE:00:10:70' + ' -I') #bluetooth connect
   bleconnect(tool,Temp1,war1,1) #bluetooth connect
   
   t=t+1
   ty1 = np.append(ty1,t) #append x axis
   tx1 = np.append(tx1,d) #append y axis
   chart1()  #plot a chart

   ud1 = threading.Thread(target = upload(d,1)) #use upload.py's function
   ud1.start() 
   
   tool1 = pexpect.spawn('gatttool -t random -b ' + 'C0:26:DE:00:0B:A4' + ' -I') #bluetooth connect
   bleconnect(tool1,Temp2,war2,2) #bluetooth connect
   
   ty2 = np.append(ty2,t) #append x axis
   tx2 = np.append(tx2,d) #append y axis
   chart2() #plot a chart
   
   ud2 = threading.Thread(target = upload(d,2)) #use upload.py's function
   ud2.start()
   
   time.sleep(1)
   m=1
   if t>=20:
    tt=tt+1
  self.cond.release()

def bleconnect(tool,Temp,war,user):   #bluetooth connect cmd
  tool.expect('\[LE\]>')
  tool.sendline("disconnect")
  tool.expect('\[LE\]>')
  time.sleep(0.5)
  print ("Preparing to connect")
  global x
  x=0
  while x<9 :
   tool.sendline("connect")
   x=x+1
  tool.expect("Connection successful",timeout=50)
  print ("Connection Successful")
  tool.expect("\r\n",timeout=50)
  tool.sendline("char-write-cmd 0x0f 0300")
  tool.expect("value: 06 ") 
  tool.expect("\r\n") #two expect let we can get string in the middle
  a=tool.before
  print (a)

  a0 = chr(a[0])
  a1 = chr(a[1])
  a3 = chr(a[3])
  a4 = chr(a[4])
  b=float(int(a0+a1,16))
  c=float(int(a3+a4,16))
  
  global d
  global k
  d=(c*256+b)/1000
  Temp.set(str(d))
  print (d)
  
  if d>=float(war):
   sd = threading.Thread(target = sendmail(d,user))
   sd.start()
   print ("22")
  test.update()
  tool.close(force=True)

def warning1(): #temperature warning value get function
 global war1
 war1 = hitemp1.get()
 print (war1)   
 
def warning2(): #temperature warning value get function
 global war2
 war2 = hitemp2.get()
 print (war2) 

def chart1():  #chart1 set function
 figure1 = plt.Figure(figsize=(3,2), dpi=100)
 figure1.add_subplot(111).axis([0+tt, t ,20,40])
 figure1.add_subplot(111).plot(ty1,tx1)
 chartt1 = FigureCanvasTkAgg(figure1,test)
 chartt1.get_tk_widget().grid(row=6,column=4)
 
 
def chart2(): #chart2 set function
 figure2 = plt.Figure(figsize=(3,2), dpi=100)
 figure2.add_subplot(111).axis([0+tt, t ,20,40])
 figure2.add_subplot(111).plot(ty2,tx2)
 chartt2 = FigureCanvasTkAgg(figure2,test)
 chartt2.get_tk_widget().grid(row=6,column=8)


test=Tk()
test.title("Test")
test.geometry('1080x500+0+0')
test.resizable(False, False)
test.configure(background='pink')

#阿熊的溫度顯示程式區塊
Temp1 = StringVar()
Temp1.set('00.0')
textLabel1 = Label(test)
textLabel1.config(bg='Plum',font=('Aharoni'),fg='DarkSlateGray',height=1,width=33,anchor=CENTER,relief="solid")
textLabel1.grid(row=2,column=4)
textLabel1['textvariable'] = Temp1

#兔兔的溫度顯示程式區塊
Temp2 = StringVar()
Temp2.set('00.0')
textLabel2 = Label(test)
textLabel2.config(bg='Plum',font=('Aharoni'),fg='DarkSlateGray',height=1,width=33,anchor=CENTER,relief="solid")
textLabel2.grid(row=2,column=8)
textLabel2['textvariable'] = Temp2

#阿熊警告溫度初值及顯示設定
hitemp1 = StringVar()
hitemp1.set('30')
texttemp1 = Spinbox(test)
texttemp1.config(width=4,from_=30,to=40)
texttemp1.grid(row=5,column=5,sticky=W)
texttemp1['textvariable'] = hitemp1

#兔兔警告溫度初值及顯示設定
hitemp2 = StringVar()
hitemp2.set('30')
texttemp2 = Spinbox(test)
texttemp2.config(width=4,from_=30,to=40)
texttemp2.grid(row=5,column=9,sticky=W)
texttemp2['textvariable'] = hitemp2


Button(test,text='連結',height=1,width = 6,bg='SlateBlue',activebackground='SlateBlue',command=lambda:bluetoothcn.start(),     
       fg='GhostWhite',activeforeground='GhostWhite',anchor=CENTER,font=('Aharoni',12)).grid(row=0,column=0)


label=Label(test,text=" ",bg='Pink',width=5).grid(row=2,column=0)
label=Label(test,font=('Aharoni',17),text="阿熊" + ': ',bg='Pink').grid(row=2,column=3)
label=Label(test,font=('Aharoni',17),text="度",bg='Pink').grid(row=2,column=5)
label=Label(test,text=" ",bg='Pink',width=12).grid(row=2,column=6)
label=Label(test,font=('Aharoni',17),text="兔兔" + ': ',bg='Pink').grid(row=2,column=7)
label=Label(test,font=('Aharoni',17),text="度",bg='Pink').grid(row=2,column=9)
label=Label(test,text=" ",bg='Pink',width=3).grid(row=2,column=10)
label=Label(test,text=" ",bg='Pink',width=2).grid(row=3,column=0)
label=Label(test,text=" ",bg='Pink',width=2).grid(row=4,column=0)
Button(test,text='警告溫度',height=1,width = 6,bg='SlateBlue',activebackground='SlateBlue',command=lambda:warning1(),   
       fg='GhostWhite',activeforeground='GhostWhite',anchor=CENTER,font=('Aharoni',12)).grid(row=5,column=4,sticky=E)
Button(test,text='警告溫度',height=1,width = 6,bg='SlateBlue',activebackground='SlateBlue',command=lambda:warning2(),   
       fg='GhostWhite',activeforeground='GhostWhite',anchor=CENTER,font=('Aharoni',12)).grid(row=5,column=8,sticky=E)
cond = threading.Condition()
bluetoothcn = bluetoothcn(cond)
test.mainloop()


