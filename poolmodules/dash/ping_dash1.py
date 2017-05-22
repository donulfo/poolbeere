import os
daship = "192.168.48.137"		#Cottonelle
response = os.system("ping -s 1 -i 2.3 " + daship + " >/tmp/dash_1.txt 2>&1")
