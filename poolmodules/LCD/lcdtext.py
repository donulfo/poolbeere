#!/usr/bin/python

import telnetlib;
import time;

host='127.0.0.1';
port='13666';
data = ""

tn = telnetlib.Telnet(host, port)
tn.write("hello\r");

data += tn.read_until("\n");
tn.write("screen_add DT\n");
data += tn.read_until("\n");

data += tn.read_until("\n");
tn.write("screen_set DT -heartbeat off\n");
data += tn.read_until("\n");

tn.write("widget_add DT 1 string\n");
data += tn.read_until("\n");

tn.write("widget_add DT 2 string\n");
data += tn.read_until("\n");



