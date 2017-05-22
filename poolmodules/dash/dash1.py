import os
import time

dash1_log = "/tmp/dash_1.txt"		# Cottonelle
target = open(dash1_log, 'w')
target.close()
	
dash1 = 0
button1 = 0

while True:

	button1 = os.path.getsize(dash1_log)
	if button1 != dash1:
		print (str(button1) + ": Button 1 Cottonelle pressed")
		dash1 = button1

	time.sleep( 5 )