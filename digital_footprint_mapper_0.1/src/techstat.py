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
import time
import MySQLdb
from subroutines import *

db = MySQLdb.connect(host,username,password,database)
d_list = []
query_list = []

def techstat():
	tech_type = get_technologytype()
	uri_file = open("output/uri_list.txt","r")

	uri_data = uri_file.readline()
	'''domain = uri_data[uri_data.find("://")+3:uri_data.find("/",8)]
	d_list.append(domain)
	data = uri_data[uri_data.rfind("/")+1:-1]
	match = check_file(data,tech_type,1)
	if match:
		query_list.append(domain+"::"+match+"::"+1)'''

	while uri_data:
		data = uri_data[uri_data.rfind("/")+1:-1]
                match = check_file(data,tech_type,1)
		domain = uri_data[uri_data.find("://")+3:uri_data.find("/",8)]
		print "[$]Stats for domain: "+domain
		if match:
			if domain+"::"+match in d_list:
				index_val = d_list.index(domain+"::"+match)
				temp = query_list[index_val]
				parameter = temp.split("::")	
				number = int(parameter[2])+1
				query_list[index_val] = parameter[0]+"::"+parameter[1]+"::"+str(number)
			else:
				d_list.append(domain+"::"+match)
				#index_val = d_list.index(domain)
				#query_list[index_val] = domain+"::"+match+"::"+str(1)
				query_list.append(domain+"::"+match+"::"+str(1))
			#print uri_data[uri_data.find("://")+3:uri_data.find("/",8)]+"::"+match
 		clear(0)
		uri_data = uri_file.readline()
	update_database()

def update_database():
	loop = 0
	while loop < len(query_list):
		parameter = query_list[loop].split("::")
		cursor = db.cursor()
		sql = "insert into techstat (Domain, Tech, Count) values ('"+parameter[0]+"','"+parameter[1]+"','"+parameter[2]+"')"
		#print sql
		time.sleep(1)
		#clear(0)
		try:
			cursor.execute(sql)
		except Exception:
			print "[*] Error Updating Database"
			time.sleep(1)
			clear(0)
	
		db.commit()
		loop+=1
		 	
