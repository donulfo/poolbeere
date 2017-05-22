#!/bin/bash

#Zwischenstatus 1 sek entspricht ca. 0,25l

watersystem=$(mysql pool -uroot -pibo43har -se "select wert from config where schluessel='watersystem';")
echo "Watersystem: " $watersystem

if [ $watersystem == "off" ]
then
	exit 1
fi

Stunde=`date +%H`
Minute=`date +%M`
d=`date +%Y-%m-%d`
t=`date +%H:%M:%S`

ws_hochbeet=$(mysql pool -uroot -pibo43har -se "select wert from config where schluessel='WS_Hochbeet';")
echo "Hcohbeet: " $ws_hochbeet
ws_tomaten=$(mysql pool -uroot -pibo43har -se "select wert from config where schluessel='WS_Tomaten';")
echo "Tomaten: " $ws_tomaten

while read line; do
	var=$line
done < "/tmp/daycount.txt"
#echo $line

weather_date=$(mysql garten -uroot -pibo43har -se "select DATE_FORMAT(weather.timestamp,'%Y-%m-%d') from weather order by timestamp DESC Limit 1;")
if [ $d == $weather_date ]
then
	will_rain3=$(mysql garten -uroot -pibo43har -se "SELECT rainfc3 FROM weather ORDER BY timestamp DESC Limit 1;")
	echo "Will rain (3h)? " $will_rain3
#	will_rain5=$(mysql garten -uroot -pibo43har -se "SELECT rainfc5 FROM weather ORDER BY timestamp DESC Limit 1;")
#	echo "Will rain (5h)? " $will_rain5
else
	will_rain3 = 0
#	will_rain5 = 0
fi


ignore_daycount="0"
sek="0"
#echo $Minute

if [ $Stunde -lt 9 ]
then
  # morgens vor 9 Uhr - giessen
  sek="40"
else
  # ab 9 Uhr (fuer abends gedacht)
  if [ $line -ge 66 ]
  then
	#echo "ab 9 und >=66"
	# mindestens 33x den hoechsten Temperatur Schwellwert überschritten (aktuell 22 Grad) = doppelt giessen
	sek="80"
  elif [ $line -ge 30 ]
  then
	#echo "ab 9 und >=30"
	# mindestens 30x den normalen Temperatur Schwellwert überschritten (aktuell 18 Grad) = giessen
	sek="40"
  elif [ $Stunde == 15 ] && [ $Minute -lt 5 ] && [ $line -ge 12 ]
  then 
	#echo "15 Uhr und >= 12"
	# um 15 Uhr schon mindestens 12x den Temperatur Schwellwert überschritten = 1/2 giessen
	#sollte es aber die naechsten 3 Stunden regnen, dann nicht
	if [ $will_rain3 == 1 ]
	then
	  sek="0"
	  #ausser es ist schon zu trocken! pruefe bodenfeuchte
	  ignore_daycount="1"
	else
	  sek="20"
	fi
  else
	echo $d $t": ab 9, aber <30"

	#falls daycount <30 aber nach 19 Uhr veranlasse Bodenfeuchte-Pruefung
	if [ $Stunde -ge 19 ]; then
	    ignore_daycount="1"
	fi
	
  fi
fi

hbsek=$sek
tomsek=$sek

# Prüfe Bodenfeuchte

if [ $ws_hochbeet == "on" ]; then
	hochbeet_date=$(mysql garten -uroot -pibo43har -se "select DATE_FORMAT(plants.timestamp,'%Y-%m-%d') from plants where sensor_name = 'Hochbeet' order by timestamp DESC Limit 1;")
	if [ $d == $hochbeet_date ]
	then
		hochbeet_moi=$(mysql garten -uroot -pibo43har -se "select water from plants where sensor_name = 'Hochbeet' order by timestamp DESC Limit 1;")
		
		if [ $hochbeet_moi -lt 25 ] && [ $ignore_daycount == "1" ]; then
			hbsek="40"
		elif [ $hochbeet_moi -ge 40 ]; then
			#echo $hochbeet_date: MOI $hochbeet_moi
			echo "Hochbeet Moisture >=40 ($hochbeet_moi), watering disabled"
			ws_hochbeet="off"
		else
		    echo "Hochbeet "$hochbeet_moi": no water needed"
		fi
	fi
fi

if [ $ws_tomaten == "on" ]; then
	tomaten_date=$(mysql garten -uroot -pibo43har -se "select DATE_FORMAT(plants.timestamp,'%Y-%m-%d') from plants where sensor_name = 'Tomaten' order by timestamp DESC Limit 1;")
	if [ $d == $tomaten_date ]
	then
		tomaten_moi=$(mysql garten -uroot -pibo43har -se "select water from plants where sensor_name = 'Tomaten' order by timestamp DESC Limit 1;")
		
		if [ $tomaten_moi -lt 25 ] && [ $ignore_daycount == "1" ]; then
			tomsek="40"
		elif [ $tomaten_moi -ge 40 ]; then
			#echo $Tomaten_date: MOI $tomaten_moi
			echo "Tomaten Moisture >=40 ($tomaten_moi), watering disabled"
			ws_tomaten="off"
		else
		    echo "Tomaten "$tomaten_moi": no water needed"
		fi
	fi
fi


# Wasserstand pruefen und ggf reagieren

if [ $sek != "0" ]
then
	while read water; do
		var=$water
	done < "/tmp/rainwater.txt"

	if [ $water -ge 70 ]
	then
		#everything good
		echo "Normal watering"
	elif [ $water -ge 50 ]
	then
		if [ $sek -ge 41 ]; then
		    hbsek="40"
		    tomsek="40"
		    python /usr/local/sbin/mail/sendmail.py marcus.schraml@schraml-it.de POOL-PI: Regenfass-Wasserstand gering, nur einfache Bewässerung möglich!
		fi
	elif [ $water -ge 30 ]
	then
		hbsek="20"
		tomsek="20"
		python /usr/local/sbin/mail/sendmail.py marcus.schraml@schraml-it.de POOL-PI: Regenfass-Wasserstand gering, nur minimale Bewässerung möglich!
	else
		sek="0"
		hbsek="0"
		tomsek="0"
		python /usr/local/sbin/mail/sendmail.py marcus.schraml@schraml-it.de POOL-PI: Regenfass-Wasserstand zu gering, keine Bewässerung möglich!
	fi
fi

	
# giessen

if [ $sek == "0" ]
then
	exit 1
fi

pumpsek="0"
if [ $ws_hochbeet == "on" ]
then
  sqlresult=$(mysql garten -uroot -pibo43har -se "insert into rainwaterpump (date,time,GPIO,logentry,value) values ('$d' , '$t', 'Power12' , 'Hochbeet gegossen' , $hbsek);")
  let pumpsek=$pumpsek+$hbsek
  #echo $line
  #echo "power on " $hbsek
  #Schalte Regenfasspumpe ein
  sudo sispmctl -d 1 -o 1
  sudo echo $d $t" Power1-1	Rainwaterpump		Power on "$hbsek>>/var/log/rainwaterpump.log
  #Magnetventil Hochbeet auf
  sudo sispmctl -d 1 -o 2
  sudo echo $d $t" Power1-2	MagVent Hochbeet	Power on "$hbsek>>/var/log/rainwaterpump.log

  #...warte def. zeitspanne
  sudo sleep $hbsek"s"

  t=`date +%H:%M:%S`

  #Schalte Pumpe aus
  sudo sispmctl -d 1 -f 1
  sudo echo $d $t" Power3	Rainwaterpump		Power off">>/var/log/rainwaterpump.log

  #Magnetventil Tomaten zu
  sudo sispmctl -d 1 -f 2
  sudo echo $d $t" Power1-2	MagVent Hochbeet	Power off "$hbsek>>/var/log/rainwaterpump.log

fi

if [ $ws_tomaten == "on" ]
then
  sqlresult=$(mysql garten -uroot -pibo43har -se "insert into rainwaterpump (date,time,GPIO,logentry,value) values ('$d' , '$t', 'Power13' , 'Tomaten gegossen' , $tomsek);")
  let pumpsek=$pumpsek+$tomsek
  #Schalte Regenfasspumpe ein
  sudo sispmctl -d 1 -o 1
  sudo echo $d $t" Power1-1	Rainwaterpump		Power on "$tomsek>>/var/log/rainwaterpump.log
  #Magnetventil Tomaten auf
  sudo sispmctl -d 1 -o 3
  sudo echo $d $t" Power1-3	MagVent Tomaten		Power on "$tomsek>>/var/log/rainwaterpump.log

  #...warte def. zeitspanne
  sudo sleep $tomsek"s"

  t=`date +%H:%M:%S`

  #Schalte Pumpe aus
  sudo sispmctl -d 1 -f 1
  sudo echo $d $t" Power3	Rainwaterpump		Power off">>/var/log/rainwaterpump.log

  #Magnetventil Tomaten zu
  sudo sispmctl -d 1 -f 3
  sudo echo $d $t" Power1-3	MagVent Tomaten		Power off "$tomsek>>/var/log/rainwaterpump.log

fi


sqlresult=$(mysql garten -uroot -pibo43har -se "insert into rainwaterpump (date,time,GPIO,logentry,value) values ('$d' , '$t', 'Power11' , 'Regenfasspumpe gelaufen' , $pumpsek);")
	
#mysql -uroot -pibo43har garten << EOF
#insert into rainwaterpump (date,time,GPIO,logentry,value) values ('$d' , '$t', 'Power3' , 'Regenfasspumpe gelaufen' , $sek);
#EOF


#echo $sek"s"