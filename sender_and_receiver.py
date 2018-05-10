import dweepy, random, time
from threading import Thread
from grovepi import*
from grove_rgb_lcd import*
from math import isnan

publisher_state = False
led = 5
pinMode(led, "OUTPUT")
digitalWrite(led,0)

setRGB(0,0,0)
setText("")

#dht = temp/humid sensor
dht_sensor_port = 7
dht_sensor_type = 0

btn = 8
pinMode(btn, "INPUT")

#True = Sensor On, False = Sensor Off
dhtSensor = True #all on by default, can be turned off by app
ultSensor = True
btnSensor = True

sampleRate = 5 #one sample every 5 seconds

def listener(publisher):
    print("==READY==")
    
    for dweet in dweepy.listen_for_dweets_from('Lawlor'): #listens for extracts content from dweets
        content = dweet["content"]
        input = content["input"]
	type = content["type"]

	#start publisher thread (by default will sample but not publish to dweet.io)
	if not publisher.is_alive():
	    publisher = Thread(target=publisher_method_dan)
	    publisher.start()

	if type == "publish":
            if input == "true":
                #updateSensors(LED_state)
                # start publishing
                global publisher_state
                publisher_state = True
            else:
                publisher_state = False
                print "wasn't true"
	elif type == "sample": #modify sample rate
	    global sampleRate
	    sampleRate = int(input)
	else:
	    updateSensors(type, input)

def publisher_method_dan():
    while True:
	time.sleep(int(sampleRate))
	if publisher_state == True:
            result = dweepy.dweet_for('Lawlor', getReadings())
	else:
	    result = getReadings();
        print result
        
def getReadings(): #retrieves readings from sensors
    dict = {}

    dict["LED"] = getLed()
    dict["Temp"] = getTempHum("temp")
    dict["Hum"] = getTempHum("hum")
    dict["Ultrasonic"] = getUltra()
    dict["Button"] = getBtn()
    return dict

publisher_thread = Thread(target=publisher_method_dan)
listener_thread = Thread(target=listener, args=(publisher_thread,))
listener_thread.start()
