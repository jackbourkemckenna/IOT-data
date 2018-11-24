import grovepi
from grovepi import *
from grove_rgb_lcd import *
from time import sleep
from math import isnan
import csv
import  socket, struct, dweepy, time, platform, random
import sqlite3
from sqlite3 import Error
from subprocess import call
thingName  = []
thingRate = []
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
#read in users config options
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
#reading Sonic data from pi
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
#get tempeture and humidity
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
#just get humidity
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
#get light data
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
#populate the tables with sensor data
def data_entry():

    c.execute("INSERT INTO data(sonic, light,temp,hum)VALUES (?,?,?,?)",(getSonic(),getlight(),gettemp(),gethum()))
    conn.commit()

while True:
    dict = getReadings()
    post(dict)
    time.sleep(thingRate)
    data_entry()
