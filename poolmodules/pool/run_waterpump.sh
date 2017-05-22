#!/bin/bash

while read line; do
    var=$line
done < "/tmp/daycount.txt"
#echo $line
sudo cp "/tmp/daycount.txt" "/tmp/daycount_yd.txt"

Stunde=`date +%H`
Minute=`date +%M`
d=`date +%Y-%m-%d`
t=`date +%H:%M:%S`

sek="0s"
#echo $Minute

if [ $Stunde -lt 9 ]
then
  # morgens vor 9 Uhr - giessen
  sek="39s"
else
  # ab 9 Uhr (fuer abends gedacht)
  if [ $line -ge 66 ]
  then
    #echo "ab 9 und >=66"
    # mindestens 33x den Temperatur Schwellwert überschritten (aktuell 30 Grad) = doppelt giessen
    sek="79s"
  elif [ $line -ge 30 ]
  then
    #echo "ab 9 und >=30"
    # mindestens 30x den Temperatur Schwellwert überschritten (aktuell 15 Grad) = giessen
    sek="39s"
  elif [ $Stunde == 15 ] && [ $Minute -lt 5 ] && [ $line -ge 12 ]
  then 
    #echo "15 Uhr und >= 12"
    # um 15 Uhr schon mindestens 12x den Temperatur Schwellwert überschritten = 1/2 giessen
    sek="19s"
  else
    echo $d $t": ab 9, aber <30"
  fi
fi

# in minuten umrechnen und in datenbank schreiben

if [ $sek == "79s" ] 
then 
  value=2 
elif [ $sek == "39s" ] 
then 
  value=1 
else 
  value=0
fi

mysql -uroot -pibo43har garten << EOF
insert into rainwaterpump (date,time,GPIO,logentry,value) values ('$d' , '$t', 'Power3' , 'Regenfasspumpe gelaufen' , $value);
EOF

# giessen

if [ $sek != "0s" ]
then
  #echo "power on " $sek
  #Schalte Regenfasspumpe ein
  sudo sispmctl -o 3
  sudo echo $d $t" Power3	Rainwaterpump		Power on "$sek>>/var/log/rainwaterpump.log

  #...warte def. zeitspanne
  sudo sleep $sek

  t=`date +%H:%M:%S`

  #Schalte Pumpe aus
  sudo sispmctl -f 3
  sudo echo $d $t" Power3	Rainwaterpump		Power off">>/var/log/rainwaterpump.log
fi
