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
import time
import MySQLdb
import time
from subroutines import *

db = MySQLdb.connect(host,username,password,database)

whois_db_string=""

def domainwhois():
	global whois_db_string, keyword
	domain_read = open("output/domain_list.txt", "r")
	domain = domain_read.readline()
	domain_keyword = open("conf/domain_whois.txt", "r")
	keyword = domain_keyword.readlines()
	db_string="Domain::Not-Available##Registrar_Whois::Not-Available##Registrar_Url::Not-Available##Updated_Data::Not-Available##Creation_Date::Not-Available##Expiration_Date::Not-Available##Registrar::Not-Available##Registrar_Email::Not-Available##Registrar_Phone::Not-Available##Registrar_Country::Not-Available##Registrant_Name::Not-Available##Registrant_Org::Not-Available##Registrant_City::Not-Available##Registrant_State::Not-Available##Registrant_Country::Not-Available##Registrant_Phone::Not-Available##Registrant_Fax::Not-Available##Registrant_Email::Not-Available##Admin_Name::Not-Available##Admin_Org::Not-Available##Admin_City::Not-Available##Admin_State::Not-Available##Admin_Country::Not-Available##Admin_Phone::Not-Available##Admin_Fax::Not-Available##Admin_Email::Not-Available##Tech_Name::Not-Available##Tech_Org::Not-Available##Tech_City::Not-Available##Tech_State::Not-Available##Tech_Country::Not-Available##Tech_Phone::Not-Available##Tech_Fax::Not-Available##Tech_Email::Not-Available##state::Not-Available##admin_c::Not-Available##tech_c::Not-Available##billing_c::Not-Available"
	while domain:
		print "[$]Domain :"+domain
		cmd = formwhois_cmd(domain)
		clear(0)
		whois_db_string=db_string
		whois_db_string=whois_db_string.replace("Domain::Not-Available","Domain::"+domain.strip("\n"))
		time.sleep(15)
		#cmd = "whois "+domain.strip("\n")
		status, output = commands.getstatusoutput(cmd.rstrip(";"))
		whois_data = output.split("\n")
		key_loop = 0
		while key_loop < len(keyword):
			temp = keyword[key_loop].split(":DB:")
			row=temp[0]	
			row_keyword=temp[1]
			if "#OR#" in row_keyword:
				sub_key=row_keyword.split("#OR#")
				subkey_loop = 0
				while subkey_loop < len(sub_key):
					match(row,sub_key[subkey_loop],whois_data)
					subkey_loop+=1		
			else:
				match(row,row_keyword,whois_data)
			key_loop+=1
		#print whois_db_string
		update_database(whois_db_string)
		whois_db_string=db_string
		clear(0)
		domain = domain_read.readline()

def match (row, data,whois_data):
	global whois_db_string
	whois_loop = 0
	while whois_loop < len(whois_data):
		if data.strip("\n") in whois_data[whois_loop] and ":" in whois_data[whois_loop] and "http://www.internic.net" not in whois_data[whois_loop]:
				val = whois_data[whois_loop].split(":",1)
				if val[1]:
					whois_db_string=whois_db_string.replace(row+"::Not-Available",row+"::"+val[1].strip(" "))
					#print row+" "+data+" "+val[1]
					break
		whois_loop+=1

def update_database(updatedb):
	global keyword
        try:
		loop=0
		rows="Domain,"
		#format_specifier=""
		value=""
		#print len(keyword)
		while loop < len(keyword):
			key=keyword[loop].split(":DB:")
			rows=rows+key[0]+","
			#format_specifier=format_specifier+"'%s',"
			loop+=1
		
		loop=0
		r_value=updatedb.split("##")
		#print len(r_value)
		while loop < len(r_value):
			temp=r_value[loop].split("::")
			value=value+"'"+temp[1]+"'"+","
			loop+=1

		#print rows
		#print format_specifier
		#print value
		cursor = db.cursor()
		#print "Inserting"
		sql = "insert into domainwhois ("+rows.strip(",")+") values ("+value.strip(",")+")"
		#print sql	
		#time.sleep(2)
		#clear(0)
		cursor.execute(sql)
		db.commit()
	except Exception:
                print " Duplicate values, database not updated !"
		time.sleep(2)
		clear(0)
                db.rollback()

def formwhois_cmd(domain):
	loop=0
	dlen = domain.count(".")
	temp=domain.split(".")
	tempstr=""
	whois_str=""
	while dlen+1 > 0:
		tempstr=temp[dlen].strip("\n")+"."+tempstr
		if tempstr.count(".") >= 2:
			whois_str=whois_str+"whois "+tempstr.rstrip(".")+";"
		dlen-=1
	return whois_str

