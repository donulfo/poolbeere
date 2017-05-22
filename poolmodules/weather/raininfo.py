# -*- coding: utf-8 -*-

import pyowm
import MySQLdb as mdb

conn = mdb.connect(host= "localhost",
				  user="root",
				  passwd="ibo43har",
				  db="garten")
x = conn.cursor()

OWMweatherAPI = '745d3030ab58e0f208988010ac73f392'  # Achtung_Sebastians API Key in Verwendung
city = 'Feldkirchen-Westerham,de'
from datetime import datetime, timedelta
owm = pyowm.OWM(OWMweatherAPI)

def checkweather():

	#### Wetterdaten Echtzeit ####
	
	obs = owm.weather_at_coords(47.91663,11.884514)
	w = obs.get_weather()
	w_status = str(w.get_status())
	w_wind_speed = str(w.get_wind()['speed'])
	w_wind_deg = str(w.get_wind()['deg'])
	w_temp = str(w.get_temperature(unit='celsius')['temp'])
	w_temp_max = str(w.get_temperature(unit='celsius')['temp_max'])

	try:
		w_rain_float = float(str(w.get_rain()))
		w_rain = str(w_rain_float)
	except:
		w_rain = "0"

	w_weather_code = str(w.get_weather_code())
	#w_icon = "http://openweathermap.org/img/w/" + str(w.get_weather_icon_name()) + ".png"
	w_icon = str(w.get_weather_icon_name()) + ".png"
	
	#### Wetterdaten Forecast ####
	
	fc3 = owm.three_hours_forecast(city)
	f = fc3.get_forecast()
	timenow = datetime.now()    #aktuelleZEIT
	timenew = timenow
	i = 1
	wbr3 = "0"
	wbr5 = "0"
	
	while i<=5:
		timenew = timenow + timedelta(hours=i)
		timenewsend = timenew.strftime("%Y-%m-%d %H:%M:00+00")
		#print ('will it be rainy at ' + timenewsend + ' in ' + city + ": " + str(fc3.will_be_rainy_at(timenewsend)) + " - " + str(i))
		if fc3.will_be_rainy_at(timenewsend) == True or fc3.will_be_snowy_at(timenewsend) == True:
			if i<=3:
				wbr3 = "1"
			else:
				wbr5 = "1"
		i = i +1	


	sql = "INSERT INTO weather (status,wind_speed,wind_deg,temp,temp_max,rain,weather_code,icon,rainfc3,rainfc5) VALUES('"\
	      + w_status + "'," + w_wind_speed + "," + w_wind_deg + "," + w_temp + "," + w_temp_max + "," + w_rain + "," + w_weather_code + ",'" + w_icon + "'," + wbr3 + "," + wbr5 + ");"
	print sql
	x.execute(sql)
	x.close

	conn.commit()
	#print f.when_rain()

checkweather()


