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

# Zeitvariable definieren
lt = localtime()

pumpstate = os.system("gpio -g read 31")
print(pumpstate)

# 1-Wire Slave-Liste oeffnen
file = open('/sys/devices/w1_bus_master1/w1_master_slaves') #Verzeichniss evtl. anpassen

# 1-Wire Slaves auslesen
w1_slaves = file.readlines()

# 1-Wire Slave-Liste schliessen
file.close()

# Header fuer Bildschirmausgabe
print('Sensor ID       | Temperatur')
print('----------------------------')

# Fuer jeden 1-Wire Slave eine Ausgabe
for line in w1_slaves:

 # 1-wire Slave extrahieren
 w1_slave = line.split("\n")[0]

 # 1-wire Slave Datei oeffnen
 file = open('/sys/bus/w1/devices/' + str(w1_slave) + '/w1_slave')

 # Inhalt des 1-wire Slave File auslesen
 filecontent = file.read()

 # 1-wire Slave File schliessen
 file.close()

 # Temperatur Daten auslesen
 stringvalue = filecontent.split("\n")[1].split(" ")[9]

 # Temperatur konvertieren
 temperature = float(stringvalue[2:]) / 1000

 # Temperatur ausgeben
 print(str(w1_slave) + ' | %5.3f °C' % temperature)

 # Werte in Datei schreiben
 # Zeit und Datum erfassen
 Datum = strftime("%d.%m.%Y")
 Uhrzeit = strftime("%H:%M:%S")
 
 con = mdb.connect('localhost', 'root', 'ibo43har', 'pool');
 with con:
         cur = con.cursor()
         cur.execute("Select id from sensors where hardware_id = '" + str(w1_slave) + "'")
         sensorid = cur.fetchone()
	
	 if -50 <= temperature <= 50:
	  print("Schreibe in DB: " + '%5.3f' % temperature)
	  cur.execute("INSERT INTO temperature(sensor_id,value) VALUES('" + str(sensorid[0]) + "','" + '%5.3f' % temperature +"')")
          #cur.execute("INSERT INTO temperature(sensor_id,value) VALUES('" + str(sensorid[0]) + "','" + '%5.3f' % temperature +"')")
	 else:
	  print("Fehlmessung?: " + '%5.3f' % temperature)

 ## Textdatei oeffnen
 #fobj_out = open("temp-daten.txt","a")
 ## Daten in Textdatei schreiben
 #fobj_out.write(Datum + ", " + Uhrzeit +", " + '%5.3f °C' % temperature + ", " + str(w1_slave) + "\n")
 ## Textdatei schliessen
 #fobj_out.close()

#while True:
        
        


# Python script beenden und GNUPLOT Grafik erstellen
#os.system("gnuplot /Verzeichnis_zum GNUPLOT-Script/temp.plt")
sys.exit(0)
