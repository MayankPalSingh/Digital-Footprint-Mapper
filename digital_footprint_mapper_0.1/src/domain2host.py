'''
Copyright (C) 2014  Mayank Pal Singh, Email:mayankpalsingh74@gmail.com

This file is a part of Digital footprint mapper.

Digital footprint mapper is free software: you can redistribute it 
and/or modify it under the terms of the GNU General Public License 
as published by the Free Software Foundation, either version 3 of 
the License, or (at your option) any later version.

Digital Footprinting is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import sys
import os
import commands
import MySQLdb
from subroutines import *

db = MySQLdb.connect(host,username,password,database)

def domain2host():
	domain_read=open("output/domain_list.txt","r")
	domain = domain_read.readline()
	while domain:
		print "[$]Domain :"+domain
		cmd="host "+domain.strip("\n")
		clear(0)
		status, output=commands.getstatusoutput(cmd)	
		data =  output.split("\n")
		loop = 0
		while loop < len(data):
			if "has address" in data[loop]:
				ip = data[loop].split(" has address ")
				update_database(domain.strip("\n"),ip[1])
				#print domain.strip("\n")+" "+ip[1]
			loop+=1
		domain = domain_read.readline()	
	db.close()

def update_database(domain,ip):
	try:
		cursor = db.cursor()
		sql = "select domain from domain2host where IP like '%s'" % (ip)
		#print sql
		#time.sleep(1)
		#clear(0)
		cursor.execute(sql)
		results=cursor.fetchall()
		val = len(results)
		if True:
			#print "Inserting"
			sql = "insert into domain2host (Domain , IP) values ('%s','%s')" % (domain,ip)	
			#print sql
			time.sleep(2)
			clear(0)
			cursor.execute(sql)
			db.commit()
	except:
		print "Error while updating database !"
		time.sleep(2)
		clear(0)
		db.rollback()
