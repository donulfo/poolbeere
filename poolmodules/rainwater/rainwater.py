# -*- coding: utf-8 -*-
#Bibliotheken einbinden
import RPi.GPIO as GPIO
import time
import os
from datetime import datetime
import MySQLdb as mdb
import subprocess

target = open('/tmp/processes.txt', 'w')
target.write(str(subprocess.check_output(['ps',  'aux'])))
target.close()

timenow = datetime.now()  #aktuelleZEIT
logtime = str(timenow.strftime("%Y-%m-%d %H:%M"))
#print timenow.strftime("%Y-%m-%d %H:%M:00+00")

def writelog(logtext_as_string):
    with open("/tmp/rainwater.log", "a") as myfile:
        myfile.write(logtime +": " + logtext_as_string + "\n")
    myfile.close

writelog("Script started")

#GPIO Modus (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#GPIO Pins zuweisen
GPIO_TRIGGER = 18
GPIO_ECHO = 24

#Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distanz():
    # setze Trigger auf HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # setze Trigger nach 0.01ms aus LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartZeit = time.time()
    StopZeit = time.time()

    # speichere Startzeit
    while GPIO.input(GPIO_ECHO) == 0:
        StartZeit = time.time()

    # speichere Ankunftszeit
    while GPIO.input(GPIO_ECHO) == 1:
        StopZeit = time.time()

    # Zeit Differenz zwischen Start und Ankunft
    TimeElapsed = StopZeit - StartZeit
    # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
    # und durch 2 teilen, da hin und zurueck
    distanz = (TimeElapsed * 34300) / 2

    return distanz
    
count = 0
maxcounts = 0
liters = 0
#if __name__ == '__main__':
try:
    while count < 8:
        maxcounts = maxcounts + 1
        if maxcounts == 16:
            break

        abstand = distanz()
        writelog("Reading Sensor, maxcounts " + str(maxcounts) + " (%.1f cm)" % abstand)
        print ("Gemessene Entfernung = %.1f cm" % abstand)

        if abstand < 1 or abstand > 90:
            print ("Messfehler?")
            print ("Gemessene Entfernung = %.1f cm" % abstand)
            time.sleep(1)
            continue

        count = count + 1
        if count < 4:
            time.sleep(1)
            continue

        #abstand = (86 - distanz()) * 7.272
        if abstand > 54:
            abstand = (85 - abstand) * 5.482235
        else:
            abstand = ((54 - abstand) * 8.2) + (31 * 5.482235)
        #abstand = (86 - distanz()) * 7.272

        if abstand < 0:
            abstand = 0
        elif abstand > 600:
            abstand = 600

        liters = liters + abstand
	
        print ("Errechnete Liter: %.0f" % abstand)

        time.sleep(1)

    # Beim Abbruch durch STRG+C resetten
except KeyboardInterrupt:
    print("Messung vom User gestoppt")
    writelog("Messung vom User gestoppt")
    GPIO.cleanup()

except:
    print("Program abgestuerzt")
    writelog("Program abgestuerzt")
    GPIO.cleanup()
    maxcounts = 16 #zum umgehen der unteren schleife


if maxcounts < 16:
    liters = liters / 5
    print ("Durchschnittliche Liter: %.0f" % liters) 
    writelog("Durchschnittliche Liter: %.0f" % liters)
    writelog("Write to rainwater.txt")
    target = open('/tmp/rainwater.txt', 'w')
    target.write("%.0f" % abstand)
    target.close()

    if timenow.strftime("%M") == 0:							# Jede volle Stunde in DB
        writelog("Open Database")
        conn = mdb.connect(host= "localhost",
                           user="root",
                           passwd="ibo43har",
                           db="garten")
        x = conn.cursor()
        writelog("Write to Database")
        sql = "INSERT INTO rainbarrel (liter) VALUES(%.0f);" % abstand
        print sql
        x.execute(sql)
        x.close
        conn.commit()


count = 0
with open("/tmp/processes.txt", "r") as ins:
    for line in ins:
        if "rainwater.py" in line:
            count = count + 1
            if count == 2:
                logtext = logtext + logtime + ": " + line
                pid = line[8:-96] #Teilstring
                os.system("kill " + pid)
            elif count > 2:
                logtext = logtext + logtime + ": " + line
            else:
                logtext = line        

if count > 2:
    writelog("====================================================================================================================")        
    writelog(logtext[:-1])        
    writelog("====================================================================================================================")        
    writelog("Killed PID " + pid)      
    writelog("====================================================================================================================")        


writelog("Script ended")
writelog("==========================================================")
