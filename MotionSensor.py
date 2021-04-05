#from firebase import firebase
from gpiozero import MotionSensor
from gpiozero import LED
import pyrebase
import time #needs to be added 


config = {
  "apiKey": "",
  "authDomain": "cssproject-9fa41-default-rtdb.firebaseapp.com",
  "databaseURL": "https://cssproject-9fa41-default-rtdb.firebaseio.com/",
  "storageBucket": "cssproject-9fa41-default-rtdb.appspot.com"
}

firebase = pyrebase.initialize_app(config)
# Get a reference to the database service
db = firebase.database()


# import RPi.GPIO as GPIO
# import time

green_led = LED(26)
red_led = LED(13)
pir = MotionSensor (11) # the data pin
red_led.on()
green_led.off()

#url =  'https://cssproject-9fa41-default-rtdb.firebaseio.com/' #database url
#firebase = firebase.FirebaseApplication(url)#real-time datbase url
#db = firebase.database()

while True:

    pir.wait_for_motion() #pir.when_motion()
    red_led.off()
    green_led.on()
    print("Motion Detected")
    obj_temp = 38
    #obj_temp = input()
    #result = firebase.post("/Apple/tyler/temps",obj_temp)
    
    
    data={'date':"2021/02/01",'email':"ty1@gmail.com",'temp':38}
    db.child("ty Inc").child("temperature").push(data)
    
    #Final Code Idea
    #data={'State':"Motion"}
    #db.child("Tyler Inc.").child("Current State").set(data)
    
    
    #firebase.post({'date':"2021/02/01",'email':"appletist@gmail.com",'temp':38})
    #firebase.post(data)
    print(obj_temp)



    pir.wait_for_no_motion() #pir.when_no_motion()
    green_led.off()
    red_led.on()
    
    #Final Code Idea
    #data={'State':"Motion"}
    #db.child("Tyler Inc.").child("Current State").set(data)
    print("Motion Stopped")

    
    
