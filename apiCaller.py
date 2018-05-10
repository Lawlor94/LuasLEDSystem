import requests
import xml.etree.ElementTree as ET

redLineMain = ["tpt", "sdk", "mys", "gdk", "bus", "abb", "jer", "fou", "smi", "mus", "heu", "jam", "fat", "ria", "sui", "gol", "dri", "bla", "blu", "kyl", "red", "kin", "bel", "coo", "hos", "tal"]
#, "sag", "for", "cit", "cvn", "fet", "con" - taken out
redLineSoon = []
redLineMainTimes = []
redLineMainDue = []

stopIndexDueMinsAPI = {}

lastDestination = ""

class apiCaller:
 
    @staticmethod
    def pullDirection(stopName, direction):
        url = "http://luasforecasts.rpa.ie/xml/get.ashx" #api URL
        parameters = {"action": "forecast", "stop": stopName, "encrypt": "false"} #api Paremeters
        response = requests.get(url, params=parameters) #response back from API
        xml = response.content #responsed parsed
        root = ET.fromstring(xml) #root element
        
        if direction is "OUTBOUND":
            dueMinsAPI = root[2][0].get('dueMins') #finds the 3rd element under root and the first element under that element, gets attribute "dueMins"
            dest = root[2][0].get('destination') #same with attribute "destination"
        elif direction is "INBOUND":
            dueMinsAPI = root[1][0].get('dueMins')
            dest = root[1][0].get('destination')
        
        
        if dueMinsAPI == 'DUE': #API returns string 'DUE' if tram is due. Changing to 0 to keep it a list of integers
            dueMinsAPI = 0
        elif dueMinsAPI == '':
            dueMinsAPI = 999 #if there is no stop, api returns blank. Set to 999 to keep it a list of integers.
        else:
            dueMinsAPI = int(dueMinsAPI)

        arr = [dueMinsAPI, dest] #returns list of minutes until tram is due and the destination
        return arr
    
class apiLooper(object):    
    def apiLoop(object, direction): #this function loops through the function in the above class for each stop
        redLineMainDue = [] #list of all due trams - no longer used
        redLineMainTimes = [] #list of all tram times
        
        for x in redLineMain:
            dueMinsAPIandDEST = apiCaller.pullDirection(x, direction)
            dueMinsAPI = dueMinsAPIandDEST[0]
            destination = dueMinsAPIandDEST[1]
        
            redLineMainTimes.append(dueMinsAPI)
            stopIndexDueMinsAPI[redLineMain.index(x)] = dueMinsAPI
     
            
            
        #print stopIndexDueMinsAPI
        #eturn redLineMainDue
        return stopIndexDueMinsAPI
    #apiLoop()