from apiCaller import apiLooper
from LED_Controller import LED_Controller
from grovepi import*
import time

#dictionary of all 3 letter abbreviations for the API and their respective stops
redLineDict = {"tpt": "The Point", "sdk": "Spencer Dock", "mys": "Mayor Square", "gdk": "George's Dock", "bus": "Busaras", "abb": "Abbey Street", "jer": "Jervis",
               "fou": "Four Courts", "smi": "Smithfield", "mus": "Museum", "heu": "Heuston", "jam": "James", "fat": "Fatima", "ria": "Rialto", "sui": "Suir Road",
               "gol": "Golden Bridge", "dri": "Drimnagh","bla": "Blackhorse", "blu": "Bluebell", "kyl": "Kylemore", "red": "Red Cow", "kin": "Kingswood",
               "bel": "Belgard", "coo": "Cookstown","hos": "Hospital", "tal": "Tallaght", "sag": "Saggart", "for": "Fortunestown", "cit": "Citywest Campus",
               "cvn": "Cheeverstown","fet": "Fettercairn", "con": "Connolly"} 

btn = 8
pinMode(btn, "INPUT")
led = 7
pinMode(led, "OUTPUT")

direction = "INBOUND"

class RunSystem(object):
    
    t = 0 #sets time to zero for time passed calculation later
    btnReady = True #button is ready to be pressed
    
    def pushToLEDS(dictOfLEDPositionsAndDueMins, localDirection):
        l = LED_Controller()
        LED_Controller.pushArrToLEDS(l, dictOfLEDPositionsAndDueMins, localDirection)
    
    while True:
        #button for switching direction
        if digitalRead(btn) and btnReady:
            if direction is "INBOUND":
                direction = "OUTBOUND"
            else:
                direction = "INBOUND"
            btnReady = False
            t = time.time()
        #button cooldown - must wait 0.75 seconds before user can switch direction again
        if((time.time() - t) > 0.75):
            btnReady = True
                
        #runs pushToLED from LEDController - with stop information and direction
        
        x = apiLooper()
        result = apiLooper.apiLoop(x, direction)
        pushToLEDS(result,direction)
        print direction
        time.sleep(2)
        