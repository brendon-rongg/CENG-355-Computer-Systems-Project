# coding: utf-8

import RPi.GPIO as GPIO
import time
# from firebase import firebase
import pyrebase

# url = 'https://cssproject-9fa41-default-rtdb.firebaseio.com/​' #add​ your URL here

config = {
  "apiKey": "",
  "authDomain": "cssproject-9fa41-default-rtdb.firebaseapp.com",
  "databaseURL": "https://cssproject-9fa41-default-rtdb.firebaseio.com/",
  "storageBucket": "cssproject-9fa41-default-rtdb.appspot.com"
}

# firebase = firebase.FirebaseApplication(url)
firebase = pyrebase.initialize_app(config)
db = firebase.database()

# result = firebase.post("/Brendon","State","Open")
# print(result)

# In1	In2	  PWM	Out1	Out2	Mode
# H	    H	  H/L	L	     L      Short brake
# L	    H	  H	    L	     H	    CCW
# L	    H	  L	    L	     L	    Short brake
# H	    L	  H	    H	     L	    CW
# H	    L	  L	    L   	 L      Short brake
# L	    L	  H	    OFF	    OFF     Stop

ain1 = 21
ain2 = 16
en = 12
temp1 = 1
led = 19
stby = 13

# Declare the GPIO settings
GPIO.setmode(GPIO.BCM)

# Setup the GPIO pins
GPIO.setup(ain1,GPIO.OUT)
GPIO.setup(ain2,GPIO.OUT)
GPIO.setup(led,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.setup(stby, GPIO.OUT)

GPIO.output(ain1,GPIO.LOW)
GPIO.output(ain2,GPIO.LOW)
GPIO.output(led,GPIO.LOW)
GPIO.output(stby,GPIO.HIGH)

p=GPIO.PWM(en,1000)

p.start(100)
print("\n")
print("Motor controlling program online \nHardware Production Tech - CENG-317-0NE\nBrendon Rongcales - N01288965")
print("\n")

while(1):


    adminState = db.child("Brendon").child("ADMIN").child("State").get()
    curState = db.child("Brendon").child("State").child("State").get()
    print("Admin: ", adminState.val(), "Current: ", curState.val())

    adminState = adminState.val()
    curState = curState.val()

    #print("Before: ", type(adminState))
    adminState = str(adminState)
    #print("After: ", type(adminState))
    curState = str(curState)

    x='s'

    clo = "Closed"

    if adminState != curState:
        print("Comparing admin to current")
        print(adminState == "Closed")
        print(adminState == "Open")
        print("AdminType: ", type(adminState), "Closed: ",type(clo))

        if adminState == "Closed":
            if curState == "Open":
                x='c'
            print("Setting current state to stay closed")

        elif adminState == "Open":
            if curState == "Closed": #this is flawed
                x='s'
            else:
                x='o'
            print("Setting current state to closed")

    x=input("Enter state: ")

    if x=='r':
        print("run")
        if(temp1==1):
         GPIO.output(ain1,GPIO.HIGH)
         GPIO.output(ain2,GPIO.LOW)
         GPIO.output(led,GPIO.HIGH)
         # GPIO.output(stby,GPIO.HIGH)
         print("forward")
         x='z'
        else:
         GPIO.output(ain1,GPIO.LOW)
         GPIO.output(ain2,GPIO.HIGH)
         GPIO.output(led,GPIO.HIGH)
         # GPIO.output(stby,GPIO.HIGH)
         print("backward")
         x='z'

    elif x=='s':
        print("stop")
        GPIO.output(ain1,GPIO.LOW)
        GPIO.output(ain2,GPIO.LOW)
        GPIO.output(led,GPIO.LOW)
        # GPIO.output(stby,GPIO.LOW)
        x='z'

    elif x=='f':
        print("forward")
        GPIO.output(ain1,GPIO.HIGH)
        GPIO.output(ain2,GPIO.LOW)
        GPIO.output(led,GPIO.HIGH)
        # GPIO.output(stby,GPIO.HIGH)
        temp1=1
        x='z'

    elif x=='b':
        print("backward")
        GPIO.output(ain1,GPIO.LOW)
        GPIO.output(ain2,GPIO.HIGH)
        GPIO.output(led,GPIO.HIGH)
        # GPIO.output(stby,GPIO.HIGH)
        temp1=0
        x='z'

    elif x=='o':
        print("opening")
        # result = firebase.post("/Brendon/State","Open")
        data = {'State':"Open"};
        db.child("Brendon").child("State").set(data)
        openDoor()
        x='z'

    elif x=='c':
        print("closing")
        # result = firebase.post("/Brendon/State","Close")
        data = {'State':"Closed"};
        db.child("Brendon").child("State").set(data)
        closeDoor()

        x='z'

    elif x=='l':
        print("Setting duty cycle to LOW")
        p.ChangeDutyCycle(25)
        x='z'

    elif x=='m':
        print("Setting duty cycle to MEDIUM")
        p.ChangeDutyCycle(50)
        x='z'

    elif x=='h':
        print("Setting duty cycle to HIGH")
        p.ChangeDutyCycle(100)
        x='z'


    elif x=='e':
        GPIO.cleanup()
        print("GPIO Clean up")
        break

    else:
        print("Wrong input")

def openDoor:
    GPIO.output(ain1,GPIO.LOW)
    GPIO.output(ain2,GPIO.HIGH)
    GPIO.output(led,GPIO.HIGH)

    time.sleep(8.5)

    GPIO.output(ain1,GPIO.LOW)
    GPIO.output(ain2,GPIO.LOW)
    GPIO.output(led,GPIO.LOW)

def closeDoor:
    GPIO.output(ain1,GPIO.HIGH)
    GPIO.output(ain2,GPIO.LOW)
    GPIO.output(led,GPIO.HIGH)

    time.sleep(8.5)

    GPIO.output(ain1,GPIO.LOW)
    GPIO.output(ain2,GPIO.LOW)
    GPIO.output(led,GPIO.LOW)
