import pyrebase
import RPi.GPIO as GPIO
import time, sys, os
GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 24
GPIO_ECHO = 23

config = {
  "apiKey": "",
  "authDomain": "cssproject-9fa41-default-rtdb.firebaseapp.com",
  "databaseURL": "https://cssproject-9fa41-default-rtdb.firebaseio.com/",
  "storageBucket": "cssproject-9fa41-default-rtdb.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

redPin = 26
greenPin = 13

GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)

def turnOn(pin):
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    
def turnOff(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    
def red():
    turnOff(greenPin)
    turnOn(redPin)
    
def green():
    turnOff(redPin)
    turnOn(greenPin)

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

def main():
    while True:
        dist = distance()
        print ("Measured Distance = %.1f cm" % dist)
        time.sleep(0.05)
        
        if dist >= 30:
            red()
            print ("LED: Red")
        elif dist <= 30:
            green()
            print ("LED: Green") 
            result = ("%.1f cm" % dist)
            db.child("Michael").child("Distance").push(result)
            print(result)
            time.sleep(5)

main()