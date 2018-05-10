import json
import paho.mqtt.client as mqtt
import random
import time
import threading
import sys
from grovepi import *

mqttc = mqtt.Client("client1", clean_session=False)
mqttc.username_pw_set("gfcfodpd", "E92kAShanVQ8")
mqttc.connect("m20.cloudmqtt.com", "16324", 60)

#assign sensors
ultraSonic = 4
button = 8
light = 0

pinMode(button, "INPUT")
pinMode(light, "INPUT")

def pub():
    
    ultraInput = ultrasonicRead(ultraSonic)
    lightInput = analogRead(light)
    buttonInput = digitalRead(button)
    #concatonates inputs into one variable 
    concatInputs = str(ultraInput)+"/"+str(lightInput)+"/"+str(buttonInput)
    
    #publich to thread "sensor/inputs"
    mqttc.publish("sensor/inputs", payload=concatInputs)
    threading.Timer(0.5, pub).start() #creates a new thread from the "pub()" method every 0.5 seconds
        
pub()

#remove this code to test
from sensors import runSystem

#begins running the LED system
x = runSystem()
runSystem.getData(x)
