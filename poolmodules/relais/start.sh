#!/bin/bash
gpio -g write 28 1
gpio -g write 29 1
gpio -g write 30 1
gpio -g write 31 1
gpio -g mode 28 out
gpio -g mode 29 out
gpio -g mode 30 out
gpio -g mode 31 out

echo "+----------------------------------+"
echo "| Relais aktiviert!                |"
echo "| Verwendet: GPIO's 28, 29, 30, 31 |"
echo "+----------------------------------+"
