from gpiozero import CPUTemperature
from datetime import datetime
import time
import pyrebase
import math
import os

config = {
  "apiKey": "",
  "authDomain": "cssproject-9fa41-default-rtdb.firebaseapp.com",
  "databaseURL": "https://cssproject-9fa41-default-rtdb.firebaseio.com/",
  "storageBucket": "cssproject-9fa41-default-rtdb.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

company = "DEMO"

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def startUp():
    data= {
        "id": "AABBCC"
        }
    db.child(company).child("sensors").child("temperature").update(data)
    check()

def check():
    cls()
    print("WAITING ON DISTANCE!\n")
    while True:
        currentID = db.child(company).child("sensors").child("temperature").child("id").get()
        newID = db.child(company).child("sensors").child("distance").child("id").get()
        
        currentID = currentID.val()
        newID = newID.val()
        
        if (currentID != newID):
            main()

def main():
    cpu = CPUTemperature()
    print("Temperature: ", cpu.temperature)
    
    while True:
        newID = db.child(company).child("sensors").child("distance").child("id").get()
        email = db.child(company).child("sensors").child("distance").child("email").get()
        
        newID = newID.val()
        email = email.val()
        
        data = {
            "temp": math.floor(cpu.temperature), #temp your RPI temp
            "id": newID
            }
        
        userID = { #sending temp to app part of database
            "date": datetime.today().strftime('%Y/%m/%d %H:%M:%S'),
            "email": email,
            "temp": math.floor(cpu.temperature)
            }
        
        db.child(company).child("sensors").child("temperature").update(data) #setting sensors
        db.child(company).child("temperature").push(userID) #adding temp to listview on app
        
        check()
        
startUp()