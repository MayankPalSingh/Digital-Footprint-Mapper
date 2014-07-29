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

def ipwhois():
	global keyword, whois_db_string
	ip_list = fetch_ip()
	ip_keyword = open("conf/ip_whois.txt", "r")
	keyword = ip_keyword.readlines()
	db_string="IP::Not-Available##NetRange::Not-Available##CIDR::Not-Available##OriginAS::Not-Available##NetName::Not-Available##NetHandle::Not-Available##Parent::Not-Available##NetType::Not-Available##RegDate::Not-Available##Updated::Not-Available##OrgName::Not-Available##City::Not-Available##StateProv::Not-Available##PostalCode::Not-Available##Country::Not-Available##OrgAbuseHandle::Not-Available##OrgAbuseName::Not-Available##OrgAbusePhone::Not-Available##OrgAbuseEmail::Not-Available##OrgAbuseRef::Not-Available##OrgTechHandle::Not-Available##OrgTechName::Not-Available##OrgTechPhone::Not-Available##OrgTechEmail::Not-Available##OrgTechRef::Not-Available##RTechHandle::Not-Available##RTechName::Not-Available##RTechPhone::Not-Available##RTechEmail::Not-Available##RTechRef::Not-Available##RNOCHandle::Not-Available##RNOCName::Not-Available##RNOCPhone::Not-Available##RNOCEmail::Not-Available##RNOCRef::Not-Available##RAbuseHandle::Not-Available##RAbuseName::Not-Available##RAbusePhone::Not-Available##RAbuseEmail::Not-Available##admin_c::Not-Available##tech_c::Not-Available##person::Not-Available##phone::Not-Available##fax_no::Not-Available"
	loop=0
	while loop < len(ip_list):
		time.sleep(30)
		domain=ip_list[loop]		
		whois_db_string=db_string
		whois_db_string=whois_db_string.replace("IP::Not-Available","IP::"+domain.strip("\n"))
		#time.sleep(15)
		cmd = "whois "+domain.strip("\n")
		status, output = commands.getstatusoutput(cmd)
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
	#	print whois_db_string
		update_database(whois_db_string)
		whois_db_string=db_string

		loop+=1

def match (row,data,whois_data):
	global whois_db_string
	whois_loop = 0
	while whois_loop < len(whois_data):
		if data.strip("\n") in whois_data[whois_loop] and ":" in whois_data[whois_loop] and "http://www.internic.net" not in whois_data[whois_loop]:
			val = whois_data[whois_loop].split(":",1)
			if val[1]:
				whois_db_string=whois_db_string.replace(row+"::Not-Available",row+"::"+val[1].strip())
				#print row+" "+data+" "+val[1]
				break
		whois_loop+=1

def update_database(updatedb):
	global keyword
        try:
		loop=0
		rows="IP,"
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
		sql = "insert into ipwhois ("+rows.strip(",")+") values ("+value.strip(",")+")"
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

def fetch_ip():
        try:
		ip_list = []
                cursor = db.cursor()
                sql = "select ip from domain2host"
                #print sql
		#time.sleep(2)
		#clear(0)	
                cursor.execute(sql)
                results = cursor.fetchall()
		for row in results:	
			#print row[0]
			ip_list.append(row[0])
		return ip_list
        except:
                print "Error while fetching IP !"         
		time.sleep(2)
		clear(0)	
