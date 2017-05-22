# -*- coding: utf-8 -*-

import MySQLdb as mdb

conn = mdb.connect(host= "localhost",
				  user="root",
				  passwd="ibo43har",
				  db="garten")
x = conn.cursor()

linecount = 0
file = open("/tmp/plants.txt", "r")
for line in file:
    if line=='':
        break
    linecount = linecount + 1
    if linecount == 1:
        plant_name = line.strip('\n')
    if linecount == 2:
        plant_batt = line.strip('\n')
    if linecount == 3:
        plant_water = line.strip('\n')
    if linecount == 4:
        plant_temp = line.strip('\n')
    if linecount == 5:
        plant_light = line.strip('\n')

        sql = "INSERT INTO plants  (sensor_name,battery,water,temp,light) VALUES('" + plant_name + "'," + plant_batt + "," + plant_water + ",'" + plant_temp + "'," + plant_light + ");"
        x.execute(sql)
        
        linecount = 0
        #print sql
x.close
conn.commit()
