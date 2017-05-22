#!/usr/bin/python
# -*- coding: utf-8 -*-

# Die Sensoren müssen mit "modprobe w1-gpio" und "modprobe w1-therm" aktiviert werden!
# NEU seit 2015: Die Sensoren werden nur noch in der /boot/config.txt mit dem Eintrag 'dtoverlay=w1-gpio-pullup' aktiviert!!!

# Import der Module
import MySQLdb as mdb
import sys
import os
import glob
from time import *
import time

def create_daycounter():
    #global daycounter    # Needed to modify global copy of globvar
    with open("/tmp/daycount.txt","w") as file:
        file.writelines("0")
    file.close

def set_daycounter():
    #global daycounter    # Needed to modify global copy of globvar

    ## Textdatei oeffnen
    with open("/tmp/daycount.txt","r") as file:
        daycounterlist = file.readlines()

        daycounter = str(int(daycounterlist[0]) + 1)

    with open("/tmp/daycount.txt","w") as file:
        file.writelines(daycounter)

def move_daycounter():
    #global daycounter    # Needed to modify global copy of globvar

    ## Textdatei oeffnen
    with open("/tmp/daycount.txt","r") as readfile:
        daycounterlist = readfile.readlines()
        daycounter = str(int(daycounterlist[0]))
    readfile.close
    with open("/tmp/daycount_yd.txt","a") as writefile:
        writefile.writelines(strftime("%d.%m.%Y") + ":      " + daycounter + "\n")
    writefile.close

# Zeitvariable definieren
lt = localtime()
stunde = int(strftime("%H", lt))
minute = int(strftime("%M", lt))

if os.path.isfile("/tmp/daycount.txt") == False or stunde == 1 and minute <= 5:
    #copy daycounter
    try:
        move_daycounter()
    except:
        print "no daycount.txt availible, will create"
    create_daycounter()

# Header fuer Bildschirmausgabe
##print('Sensor ID       | Temperatur')
##print('----------------------------')

# 1-wire Slave Datei oeffnen
file = open('/sys/bus/w1/devices/28-000004ce263d/w1_slave')

# Inhalt des 1-wire Slave File auslesen
filecontent = file.read()

# 1-wire Slave File schliessen
file.close()

# Temperatur Daten auslesen
stringvalue = filecontent.split("\n")[1].split(" ")[9]

# Temperatur konvertieren
temperature = float(stringvalue[2:]) / 1000

# Temperatur ausgeben
#print('28-000004ce263d | %5.3f °C' % temperature)

# Werte in Datei schreiben
# Zeit und Datum erfassen
Datum = strftime("%d.%m.%Y")
Uhrzeit = strftime("%H:%M:%S")
 
 #con = mdb.connect('localhost', 'root', 'ibo43har', 'pool');
 #with con:
 #        cur = con.cursor()
 #        cur.execute("Select id from sensors where hardware_id = '" + str(w1_slave) + "'")
 #        sensorid = cur.fetchone()
 #	
 #	 if -50 <= temperature <= 50:
 #	  print("Schreibe in DB: " + '%5.3f' % temperature)
 #	  cur.execute("INSERT INTO temperature(sensor_id,value) VALUES('" + str(sensorid[0]) + "','" + '%5.3f' % temperature +"')")
 #        #cur.execute("INSERT INTO temperature(sensor_id,value) VALUES('" + str(sensorid[0]) + "','" + '%5.3f' % temperature +"')")
 #	 else:
 #	  print("Fehlmessung?: " + '%5.3f' % temperature)


if 14 <= stunde < 17:
    if 18 <= temperature < 40:
        #Wenn groesser 18 Grad dann erhoehe counter
        set_daycounter()
    if 22 <= temperature < 40:
        #Wenn groesser 22 Grad dann erhoehe counter nochmal
        set_daycounter()


#while True:
        
        


# Python script beenden und GNUPLOT Grafik erstellen
#os.system("gnuplot /Verzeichnis_zum GNUPLOT-Script/temp.plt")
sys.exit(0)
