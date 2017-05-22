#/bin/sh
clear
sispmctl -d 0 -g 1
sispmctl -d 0 -g 2 | grep Status
sispmctl -d 0 -g 3 | grep Status
sispmctl -d 0 -g 4 | grep Status
sispmctl -d 1 -g 1
sispmctl -d 1 -g 2 | grep Status
sispmctl -d 1 -g 3 | grep Status
sispmctl -d 1 -g 4 | grep Status
