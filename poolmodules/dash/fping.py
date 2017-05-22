import os
import time
import sys

daship1 = "192.168.99.50"				#Cottonelle
dashcommand1 = "sispmctl -d 0 -t 4"

while True:
	try:
		result = os.system("fping -b1 -c1 -t250 " + daship1 + " >/dev/null 2>&1")
		print "nix"
		if result == 0:
			print ("Button pressed")
			os.system(dashcommand1)

		time.sleep ( 0.2 )

	except KeyboardInterrupt:
		print("Vom User gestoppt")
		sys.exit()