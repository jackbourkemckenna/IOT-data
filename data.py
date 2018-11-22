import grovepi
from grovepi import *
from grove_rgb_lcd import *
from time import sleep
from math import isnan
import csv
import  socket, struct, dweepy, time, platform, random
import sqlite3
from sqlite3 import Error
thingName  = []
thingRate = [] 
#newRate = map(lambda line: [int(x) for x in line],thingRate)


from subprocess import call
def makeDB():
    conn =sqlite3.connect('PiData.db')
    print ("Database created")
makeDB()
conn = sqlite3.connect('PiData.db')
#making tables calling another script from file as I had strange bug 
call(["python", "makeTable.py"])
print("making tables")
sleep(4)

c = conn.cursor()

def create_table():
        c.execute("CREATE TABLE IF NOT EXISTS data(sonic int, light double, temp int, hum int)")
        print("tables created")
def usrConfig():
    with open('config.csv') as File: 
        reader = csv.reader(File, delimiter=',')
        next(reader,None)
        for row in reader:
            global thingName
            global thingRate
            thingName = str(row[0])
            thingRate = int(row[1])
usrConfig()        
def post(dic):
    thing = thingName
    print (dweepy.dweet_for(thing,dic))

def getSonic():
        sonic_ranger = 4
        Relay_pin = 2

        pinMode(Relay_pin,"OUTPUT")

        while True:
            try:
                distant = ultrasonicRead(sonic_ranger)
            except IOError:
                print("Error")
            return(distant)
def gettemp(): 
	sensor = 3
	blue = 0
	white = 1
	while True:
            try:
                [temp,humidity] = grovepi.dht(sensor,blue)
                if math.isnan(temp) == False and math.isnan(humidity) == False:
                    print("hmm")
            except IOError:
                print ("Error")
            return(temp)
def gethum(): 
	sensor = 3
	blue = 0
	white = 1
	while True:
            try:
                [temp,humidity] = grovepi.dht(sensor,blue)
                if math.isnan(temp) == False and math.isnan(humidity) == False:
                    print('hmmm')
            except IOError:
                print ("Error")
            return(humidity)
def getlight():    
    light_sensor= 0   
    while True: 
        try:
            sensor_value = grovepi.analogRead(light_sensor)
            resistance = (float)(1023 - sensor_value) * 10 / sensor_value
        except IOError:
            print("erro")
        return(sensor_value)

def getReadings():
    dict = {}
    dict["light"] = getlight() 
    dict["sonic"] = getSonic()
    dict["temp"] = gettemp()
    dict["hum"] = gethum()
    return dict
def create_tabliwe():
        c.execute("CREATE TABLE IF NOT EXISTS data(sonic int, light double, temp int, hum int)")

def data_entry():
    
    c.execute("INSERT INTO data(sonic, light,temp,hum)VALUES (?,?,?,?)",(getSonic(),getlight(),gettemp(),gethum()))
    conn.commit()
                                
while True:
    dict = getReadings()
    post(dict)
    time.sleep(thingRate)
    data_entry()
