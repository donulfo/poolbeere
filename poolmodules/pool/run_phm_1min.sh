#!/bin/bash

d=`date +%Y-%m-%d`
t=`date +%H:%M:%S`

#Schalte Pumpe ein
gpio -g write 29 0
gpio -g mode 29 out
sispmctl -o 1
echo $d" "$t" GPIO29	PHminus		Power on" 
php /usr/local/sbin/php_logging/gpio29_on_log.php

#...warte 1 Minute
sleep 59s

d=`date +%Y-%m-%d`
t=`date +%H:%M:%S`

#Schalte Pumpe aus
gpio -g write 29 1
gpio -g mode 29 in
sispmctl -f 1
echo $d" "$t" GPIO29	PHminus		Power off"
php /usr/local/sbin/php_logging/gpio29_off_log.php
