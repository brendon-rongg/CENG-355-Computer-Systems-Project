from gpiozero import CPUTemperature
import time
import pyrebase



config = {
  "apiKey": "",
  "authDomain": "cssproject-9fa41-default-rtdb.firebaseapp.com",
  "databaseURL": "https://cssproject-9fa41-default-rtdb.firebaseio.com/",
  "storageBucket": "cssproject-9fa41-default-rtdb.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


while(1):
    cpu = CPUTemperature()
    
    print(cpu.temperature)
    if(cpu.temperature > 50):
        data={'date':"2021/02/01",'email':"anthony@gmail.com",'temp':cpu.temperature}
        db.child("Fontana").child("temperature").child("Fever").push(data)
        print("FEVER\n")
        time.sleep(2)
    else:
        data={'date':"2021/02/01",'email':"anthony@gmail.com",'temp':cpu.temperature}
        db.child("Fontana").child("temperature").child("No_Fever").push(data)
        print("NO FEVER\n")
        time.sleep(2)
    