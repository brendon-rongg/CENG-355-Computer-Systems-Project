from gpiozero import MotionSensor
from gpiozero import LED
from datetime import datetime
import pyrebase
import time #needs to be added
import random
import string
import os

config = {
  "apiKey": "",
  "authDomain": "cssproject-9fa41-default-rtdb.firebaseapp.com",
  "databaseURL": "https://cssproject-9fa41-default-rtdb.firebaseio.com/",
  "storageBucket": "cssproject-9fa41-default-rtdb.appspot.com"
}

firebase = pyrebase.initialize_app(config)
# Get a reference to the database service
db = firebase.database()

company = "DEMO"
green_led = LED(26)
red_led = LED(13)
pir = MotionSensor(11) # the data pin
red_led.on()
green_led.off()

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def startUp():
    data= {
        "id": "AABBCC"
        }
    db.child(company).child("sensors").child("motion").update(data)
    time.sleep(10)
    check()

def check():
    cls()
    print("WAITING ON LOCK!\n")
    while True:
        currentID = db.child(company).child("sensors").child("motion").child("id").get()
        newID = db.child(company).child("sensors").child("lock").child("id").get()
        
        currentID = currentID.val()
        newID = newID.val()
        
        if (currentID == newID):
            main()
        

def main():
    letters = string.ascii_lowercase
    randomID = ''.join(random.choice(letters) for i in range(6))
    
    motion = "false"
    
    green_led.off()
    red_led.on()
    
    data= {
        'motion':"false",
        }
    db.child(company).child("sensors").child("motion").update(data)
    
    while True:
        pir.wait_for_no_motion()
        pir.wait_for_motion() #pir.when_motion()
        motion = "true"
        
        if (motion == "true"):
            red_led.off()
            green_led.on()
            print("Motion Detected")
        
            #Uploading info to database
            data= {
                'motion':"true",
                "id": randomID
                }
            db.child(company).child("sensors").child("motion").update(data)
            check()
            
startUp()