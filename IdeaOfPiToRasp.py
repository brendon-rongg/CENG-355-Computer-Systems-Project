from firebase import firebase
from gpiozero import MotionSensor
from gpiozero import LED

import RPi.GPIO as GPIO
import time
from mlx90614 import MLX90614

thermometer_address = 0x5a
thermometer = MLX90614(thermometer_address)


green_led = LED(13)
red_led = LED(26)
pir = MotionSensor (11) # the data pin
red_led.on()
green_led.off()

While True:

    pir.wait_for_motion() #pir.when_motion()
    red_led.off()
    green_led.on()
    print("Motion Detected")
    printedtemp = 38
    url =  'https://cssproject-9fa41-default-rtdb.firebaseio.com/' #database url
    firebase = firebase.firebaseApplication(url)#real-time datbase url
    
        
    #if(in range of ultrasonic sensor):"
        #obj_temp = thermometer.get_obj_temp()
        #temp_String = str(obj_temp)
        
        
        #if obj_temp < 37.6:
            #msg = "Your Temp: "+temp_String+"C"
            #msg2 = "Not A Fever"
        
            openDoor()
            # result = firebase.put("/Temp","Value",obj_temp)     
            # result = firebase.put("/Temp","email","date","Value","tyler123@gmail.com","2020/12/23",obj_temp) #have no idea if it works
            # print(result)
    
            # time.sleep(12) #sleep so person can enter 
    
            closeDoor()
        
        # #elif:
            closeDoor()
            
    #elif:
        #print("you are to far from the sensor")
    
    
    
    
    pir.wait_for_no_motion() #pir.when_no_motion()
    green_led.off()
    print("Motion Stopped")
    red_led.on()



def openDoor:
            # print("opening")
            # GPIO.output(ain1,GPIO.LOW)
            # GPIO.output(ain2,GPIO.HIGH)
            # #GPIO.output(led,GPIO.HIGH)
            # # GPIO.output(stby,GPIO.HIGH)
            # # temp1=1
            # # print("hopefully sleeping")
            # time.sleep(8.5)
            # # print("hopefully awake now")
            # GPIO.output(ain1,GPIO.LOW)
            # GPIO.output(ain2,GPIO.LOW)
            # #GPIO.output(led,GPIO.LOW)
            # # GPIO.output(stby,GPIO.LOW)
            # #x='z'


def closeDoor:
            # print("closing")
            # GPIO.output(ain1,GPIO.HIGH)
            # GPIO.output(ain2,GPIO.LOW)
            # GPIO.output(led,GPIO.HIGH)
            # # GPIO.output(stby,GPIO.HIGH)
            # # temp1=0
            # # print("hopefully sleeping")
            # time.sleep(8.5)
            # # print("hopefully awake now")
            # GPIO.output(ain1,GPIO.LOW)
            # GPIO.output(ain2,GPIO.LOW)
            # GPIO.output(led,GPIO.LOW)
            # # GPIO.output(stby,GPIO.LOW)
            # #x='z'