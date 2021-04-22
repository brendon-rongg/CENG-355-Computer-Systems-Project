import RPi.GPIO as GPIO
import time
import pyrebase
import os

#GPIO.setwarnings(False)

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

company = "DEMO"

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def fixState():
    GPIO.output(ain1,GPIO.HIGH)
    GPIO.output(ain2,GPIO.LOW)
    GPIO.output(led,GPIO.HIGH)

    time.sleep(8.5)

    GPIO.output(ain1,GPIO.LOW)
    GPIO.output(ain2,GPIO.LOW)
    GPIO.output(led,GPIO.LOW)

    check()

def openDoor():
    print("Unlocking door!")
    data = {
        'state': "open"
        }

    db.child(company).child("sensors").child("lock").update(data)

    GPIO.output(ain1,GPIO.LOW)
    GPIO.output(ain2,GPIO.HIGH)
    GPIO.output(led,GPIO.HIGH)

    time.sleep(8.5)

    GPIO.output(ain1,GPIO.LOW)
    GPIO.output(ain2,GPIO.LOW)
    time.sleep(5)
    GPIO.output(led,GPIO.LOW)

def closeDoor():
    print("Locking door!")

    newID = db.child(company).child("sensors").child("temperature").child("id").get()
    newID = newID.val()

    data = {'state': "closed",
            'id': newID
            }

    db.child(company).child("sensors").child("lock").update(data)

    GPIO.output(ain1,GPIO.HIGH)
    GPIO.output(ain2,GPIO.LOW)
    GPIO.output(led,GPIO.HIGH)

    time.sleep(8.5)

    GPIO.output(ain1,GPIO.LOW)
    GPIO.output(ain2,GPIO.LOW)
    GPIO.output(led,GPIO.LOW)

    check()

def startUp():
    data= {
        "id": "AABBCC"
        }
    db.child(company).child("sensors").child("lock").update(data)

    state = db.child(company).child("sensors").child("lock").child("state").get()
    state = state.val()
    state = str(state)

    if state == "open":
        fixState()

    check()

def check():
    cls()
    print("WAITING ON TEMPERATURE!\n")
    while True:
        currentID = db.child(company).child("sensors").child("lock").child("id").get()
        newID = db.child(company).child("sensors").child("temperature").child("id").get()

        currentID = currentID.val()
        newID = newID.val()

        if (currentID != newID):

            main()

def main():
    while True:
        astate = db.child(company).child("sensors").child("lock").child("astate").get()
        state = db.child(company).child("sensors").child("lock").child("state").get()
        inputTemp = db.child(company).child("sensors").child("temperature").child("temp").get()

        astate = astate.val()
        state = state.val()
        inputTemp = inputTemp.val()

        print("Admin State: ",astate,"\nState: ",state,"\nTemperature: ",inputTemp,"\n")
        time.sleep(3)

        astate = str(astate)
        state = str(state)

        if(astate == "closed"):
            print("Override enabled! Door remaining locked!")
            time.sleep(3)
            if(state == "open"):
                closeDoor()
            else:
                newID = db.child(company).child("sensors").child("temperature").child("id").get()
                newID = newID.val()

                data = {
                    'id': newID
                    }
                db.child(company).child("sensors").child("lock").update(data)

                check()

        if(astate == "open"):
            if (inputTemp > 60):
                print("TEMPERATURE TOO HIGH! DOOR LOCKED!")
                time.sleep(3)
                if (state == "open"):
                    closeDoor()
                else:
                    newID = db.child(company).child("sensors").child("temperature").child("id").get()
                    newID = newID.val()

                    data = {
                        'id': newID
                        }
                    db.child(company).child("sensors").child("lock").update(data)

                    check()
            else:
                if (state == "closed"):
                    openDoor()
                    closeDoor()

startUp()
