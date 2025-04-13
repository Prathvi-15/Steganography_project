import csv
import math
import random
import smtplib
from tkinter import *
import subprocess


#APP NAME AND DEVICE IN GOOGLE APP PASSWORD: Gmail on Android

def ex():
    message.set("You are Blocked")
    exit()

def mail():
    global OTP
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    otp = OTP + " is your OTP"
    msg = otp
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("johnjohnwick135@gmail.com", "bhdj udur auan wvxs")
    emailid = EMAIL.get().upper()
    with open('users.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader) # skip the header row
        for row in reader:
            if row[2] == emailid:
                s.sendmail('&&&&&&&&&&&', emailid, msg)
                message.set("Mail id is Valid, Enter OTP")
                return
    message.set("Mail id is Invalid")

def ver():
  a=VER.get()
  if a == OTP:
   message.set("OTP is Verified")
   cmd = 'python GUI_B.py'
   p = subprocess.Popen(cmd, shell=True)
   login_screen.destroy()
  else:
   message.set("Please Check your OTP again")

def Loginform():
    global login_screen
    login_screen = Tk()
    #Setting title of screen
    login_screen.title("LOGIN FOR STEGANOGRAPHY")
    #setting height and width of screen
    login_screen.geometry("400x150")
    global  message;
    global EMAIL
    global VER
    EMAIL = StringVar()
    VER = StringVar()
    message=StringVar()
    Label(login_screen, text="EMAIL ID").place(x=50,y=20)
    Entry(login_screen, textvariable=EMAIL).place(x=150,y=20)
    login_screen.login = Button(login_screen, text='GET OTP', command=mail).place(x=300, y=20)
    Label(login_screen, text="OTP").place(x=50, y=60)
    Entry(login_screen, textvariable=VER).place(x=150, y=60)
    login_screen.login = Button(login_screen, text='VERIFY', command=ver).place(x=300, y=60)
    Label(login_screen, text="STATUS AWAITING", textvariable=message,bg="black",fg="white").place(x=50, y=100)
    login_screen.mainloop()

Loginform()