#Usage: python sendmail.py mailreceipient mailsubject

import sys
#print "This is the name of the script: ", sys.argv[0]
#print "Number of arguments: ", len(sys.argv)
#print "The arguments are: " , str(sys.argv)

if len(sys.argv) < 2:
    print ""
    print "ERROR - Missing Arguments"
    print "Usage: python sendmail.py mailreceipient mailsubject"
    print ""
    sys.exit()

mailreceipient = sys.argv[1]
mailsubject = sys.argv[2]

if len(sys.argv) > 2:
    i = 3
    while i < len(sys.argv):
        #print str(i) + ". Argument ", sys.argv[i]
        mailsubject = mailsubject + " " + sys.argv[i]
        i = i + 1

import smtplib
server = smtplib.SMTP('mail.schraml-it.de', 25)

#Next, log in to the server
server.login("marcus.schraml@schraml-it.de", "Diabolo%17")

#Create Message
msg = 'Subject: {}\n\n{}'.format(mailsubject, "This mail was sent using " + sys.argv[0])

try:
    #Send the mail
    server.sendmail("POOL-PI", mailreceipient, msg)
    print ""
    print "Receipient: " + mailreceipient
    print "Subject:    " + mailsubject
    print ""
    print "Mail was sent succesfully"
    print ""
except:
    print ""
    print "ERROR - Wrong Arguments"
    print "Usage: python sendmail.py mailreceipient mailsubject"
    print ""

sys.exit()