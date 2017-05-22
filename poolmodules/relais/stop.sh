#!/bin/bash
gpio -g write 28 1
gpio -g write 29 1
gpio -g write 30 1
gpio -g write 31 1
gpio -g mode 28 in
gpio -g mode 29 in
gpio -g mode 30 in
gpio -g mode 31 in

echo "+------------------------------------+"
echo "| Relais abgeschalten                |"
echo "| Freigegebene GPIO's 28, 29, 30, 31 |"
echo "+------------------------------------+"
