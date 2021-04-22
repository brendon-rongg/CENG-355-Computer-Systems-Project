from datetime import datetime
import pyzbar.pyzbar as pyzbar
import RPi.GPIO as GPIO
import numpy as np
import pyrebase
import time, sys, os
import cv2

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

config = {
  "apiKey": "",
  "authDomain": "cssproject-9fa41-default-rtdb.firebaseapp.com",
  "databaseURL": "https://cssproject-9fa41-default-rtdb.firebaseio.com/",
  "storageBucket": "cssproject-9fa41-default-rtdb.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

company = "DEMO"

GPIO_TRIGGER = 24
GPIO_ECHO = 23
redPin = 26
greenPin = 13
bluePin = 19

GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)

cap = cv2.VideoCapture(0)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def turnOn(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    
def turnOff(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    
def red():
    turnOff(greenPin)
    turnOff(bluePin)
    turnOn(redPin)
    
def green():
    turnOff(redPin)
    turnOff(bluePin)
    turnOn(greenPin)
    
def blue():
    turnOff(redPin)
    turnOff(greenPin)
    turnOn(bluePin)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def startUp():
    data= {
        "id": "AABBCC"
        }
    db.child(company).child("sensors").child("distance").update(data)
    check()
    

def check():
    turnOff(greenPin) #turning off LEDS as they are not needed yet
    turnOff(redPin)
    
    cls()
    print("WAITING ON MOTION!\n")
    while True:
        currentID = db.child(company).child("sensors").child("distance").child("id").get()
        newID = db.child(company).child("sensors").child("motion").child("id").get()
        
        currentID = currentID.val()
        newID = newID.val()
        
        if (currentID != newID):
            main()
        
def main():    
    company = "null" #setting vars to null so it doesnt accidently send information again with current user info
    email = "null"
    x = 0 #vars needed for loop
    
    print("Scan QR code to proceed!\n")
    while True:
        _, frame = cap.read() #checks for webcam
        decodedObjects = pyzbar.decode(frame) #decodes the QR code
        #cv2.imshow("Frame", frame) #USED TO TROUBLESHOOT CAMERA
        #cv2.waitKey(27) #^^^^^^^
        for obj in decodedObjects:
            print("Data", obj.data) #prints qr code data
            userID = obj.data #setting userid to the data
            userID = userID.decode() #turning data into string
            split_id = userID.partition('-') #chopping data at specific part
            company = split_id[0] #chopping before -
            email = split_id[2] #chopping after -
            
            for x in range(50): #loop that keeps LED blue for 5 seconds
                blue()
                _, frame = cap.read() #keeping camera on so it doesnt lag and keep taking qr code
                #cv2.imshow("Frame", frame) #USED TO TROUBLESHOOT CAMERA
                #cv2.waitKey(27) #^^^^^^^
            x = 0 #setting x to 0 again to restart loop after info is stored in database
            
        if (email != "null"):
            while True:
                cls()
                dist = distance()
                print ("Measured Distance = %.1f cm" % dist,"\n")
                time.sleep(0.05)
                
                if dist >= 30:
                    red()
                    print ("LED: Red\n")
                    time.sleep(0.05)
                elif dist <= 30:
                    green()
                    print ("LED: Green\n")
                    time.sleep(0.05)
                    result = ("%.1f cm" % dist)
                    
                    newID = db.child(company).child("sensors").child("motion").child("id").get()
                    newID = newID.val()
                        
                    data = {
                        "distance": result,
                        "email": email,
                        "id": newID
                        }
                    db.child(company).child("sensors").child("distance").update(data)
                        
                    print(result)
                    time.sleep(3)
                    
                    check()

startUp()