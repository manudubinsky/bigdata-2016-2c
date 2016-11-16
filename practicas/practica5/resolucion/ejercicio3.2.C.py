#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys


con = None

try:

	con = psycopg2.connect(database='world', user='manuel', password='manuel') 

	cur = con.cursor()     
	
	cur.execute("select  (name) from country ORDER BY gnp DESC LIMIT 5")

	while True:

		row = cur.fetchone()
        
		if row == None:
			break
                       
		print row[0]   

except psycopg2.DatabaseError, e:
	print 'Error %s' % e    
	sys.exit(1)
    
    
finally:
    
	if con:
		con.close()
