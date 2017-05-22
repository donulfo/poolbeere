#'print("Getting data from Mi Flora")
#'print("FW: {}".format(poller.firmware_version()))
#'print("Name: {}".format(poller.name()))
#'print("Temperature: {}".format(poller.parameter_value("temperature")))
#'print("Feuchtigkeit in Prozent: {}".format(poller.parameter_value(MI_MOISTURE)))
#'print("Light: {}".format(poller.parameter_value(MI_LIGHT)))
#'print("Naehrstatus: {}".format(poller.parameter_value(MI_CONDUCTIVITY)))
#'print("Battery: {}".format(poller.parameter_value(MI_BATTERY)))

import os    
import datetime

from miflora_poller import MiFloraPoller, \
    MI_CONDUCTIVITY, MI_MOISTURE, MI_LIGHT, MI_TEMPERATURE, MI_BATTERY

hochbeet_id = "C4:7C:8D:61:A1:AC"
tomato_id = "C4:7C:8D:61:A0:E4"
chili_id = "C4:7C:8D:63:7D:3B"

os.system("rm /tmp/plants.txt")

try:
    poller = MiFloraPoller(hochbeet_id)
    hochbeet_batt = format(poller.parameter_value(MI_BATTERY))
    hochbeet_water = format(poller.parameter_value(MI_MOISTURE))
    hochbeet_temp =  format(poller.parameter_value("temperature"))
    hochbeet_light =  format(poller.parameter_value(MI_LIGHT))
    print ('Hochbeet: ' + hochbeet_id + ', ' + hochbeet_batt + ', ' + hochbeet_water + ', ' + hochbeet_temp)

    poller = MiFloraPoller(tomato_id)
    tomato_batt = format(poller.parameter_value(MI_BATTERY))
    tomato_water = format(poller.parameter_value(MI_MOISTURE))
    tomato_temp =  format(poller.parameter_value("temperature"))
    tomato_light =  format(poller.parameter_value(MI_LIGHT))
    print ("Tomaten:  " + tomato_id + ", " + tomato_batt + ", " + tomato_water + ", " + tomato_temp)

    poller = MiFloraPoller(chili_id)
    chili_batt = format(poller.parameter_value(MI_BATTERY))
    chili_water = format(poller.parameter_value(MI_MOISTURE))
    chili_temp =  format(poller.parameter_value("temperature"))
    chili_light =  format(poller.parameter_value(MI_LIGHT))
    print ('Chilies: ' + chili_id + ', ' + chili_batt + ', ' + chili_water + ', ' + chili_temp)

    f = open('/tmp/plants.txt', 'w')
    f.write('Hochbeet\n')                     # python will convert \n to os.linesep
    f.write(hochbeet_batt + '\n')
    f.write(hochbeet_water + '\n')
    f.write(hochbeet_temp + '\n')
    f.write(hochbeet_light + '\n')
    f.write('Tomaten\n')
    f.write(tomato_batt + '\n')
    f.write(tomato_water + '\n')
    f.write(tomato_temp + '\n')
    f.write(tomato_light + '\n')
    f.write('Chilies\n')
    f.write(chili_batt + '\n')
    f.write(chili_water + '\n')
    f.write(chili_temp + '\n')
    f.write(chili_light + '\n')
    f.close()                                 # you can omit in most cases as the destructor will call it

    stunde = datetime.datetime.now().strftime("%H")
    if int(stunde) > 19:
        if int(hochbeet_batt) < 20:
            os.system("python /usr/local/sbin/mail/sendmail.py marcus.schraml@schraml-it.de POOL-PI: Batterie Hochbeet unter 20%!")
        if int(tomato_batt) < 20:
            os.system("python /usr/local/sbin/mail/sendmail.py marcus.schraml@schraml-it.de POOL-PI: Batterie Tomaten unter 20%!")
        if int(chili_batt) < 20:
            os.system("python /usr/local/sbin/mail/sendmail.py marcus.schraml@schraml-it.de POOL-PI: Batterie Chilis unter 20%!")

    os.system("python /usr/local/sbin/miflora/write_plantsdb.py")

except:
    print ("Error reading Devices")
