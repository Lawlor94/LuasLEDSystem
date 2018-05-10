import time

from neopixel import *

import argparse
import signal
import sys

from grovepi import *

def signal_handler(signal, frame):
    colorWipe(strip, Color(0,0,0))
    sys.exit(0)

def  opt_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
    if args.c:
        signal.signal(signal.SIGINT, signal_handler)
        
# LED Strip Configurations
LED_COUNT      = 40      # Number of LED pixels
LED_PIN        = 18      # GPIO pin connected to strip
LED_FREQ_HZ    = 800000  # LED signal freq. in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal
LED_BRIGHTNESS = 200   
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0	 # set to 1 for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB # Strip type and colour ordering

#Process Arguments
opt_parse()



#Create NeoPixel object with config above
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
# Initialize the library (must be called once before other functions)
strip.begin()

class LED_Controller(object):
    
    def pushArrToLEDS(object, dictOfLedPositionsAndDueMins, direction):
            #print dictOfLedPositionsAndDueMins
        #while True:
            object.adjustBrightness() #adjust brightness of LEDs based on outside brightness
            
            color = Color(0,0,0) #default color (off)
            
            
            for i in range(0, LED_COUNT): #sets all LEDs to blank
                strip.setPixelColor(i, color)
            
            if object.userIsNear() is True: #if theres a user near
                for key,val in dictOfLedPositionsAndDueMins.items(): #sets color of each individual light based on stop data
                    if val != 0 and val != 999: #if there is a tram coming and it is not currently due
                        color = Color((160/(val*8)),0,0) #color gets dimmer the higher the value (minutes until tram arrives)
                    elif val == 0:
                        color = Color(15,15,15) #LED turns white if tram is due. Numbers are lower as to display white all led LEDs are used for R, G and B. This affects brightness
                    else:
                        color = Color(0,0,0) #if there is no tram coming turn off LED
                    strip.setPixelColor(key, color)
                
                
                
                
            strip.show() #pushes changes to LED
            print "========="
    #adjusts brightness based on light sensor reading
    def adjustBrightness(object):
        lightSensor = 0
        pinMode(lightSensor,"INPUT")
        brightness = analogRead(lightSensor)
            
        #light level is in 3 steps
        if brightness > 500:
            LED_BRIGHTNESS = 240 # Brightness on a scale of 0 to 255
        elif brightness <= 500 and brightness > 150:
            LED_BRIGHTNESS = 60
        else:
            LED_BRIGHTNESS = 1
        
        print "LED Brightness: "
        print LED_BRIGHTNESS
        #strip must be restarted to change brightness
        strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
        strip.begin()
    
    #returns true if object is close to sensor
    def userIsNear(object):
        ultraSensor = 4
        distance = ultrasonicRead(ultraSensor)        
        if distance > 100:
            print "User not near"
            return False
            
        else:
            print "User near"
            return True