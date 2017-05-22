from scapy.all import *
import os

def arp_display(pkt):
 if pkt.haslayer(ARP):
  if pkt[ARP].op == 1: #who-has (request)
    if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
      print(pkt[ARP].hwsrc)
      if pkt[ARP].hwsrc == '74:75:48:5f:99:30': # Cottonelle
        print "Pushed Cottonelle"
        #Power-Toggle Filterpumpe
        os.system("sispmctl -d 0 -t 4")
      elif pkt[ARP].hwsrc == '10:ae:60:00:4d:f3': # Elements
        print "Pushed Elements"
      else:
        print "ARP Probe from unknown device: " + pkt[ARP].hwsrc

print ("waiting...")
print sniff(prn=arp_display, filter="arp", store=0, count=10)
