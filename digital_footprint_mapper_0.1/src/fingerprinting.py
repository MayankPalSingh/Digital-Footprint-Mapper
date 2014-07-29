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
import Queue
from subroutines import *

db = MySQLdb.connect(host,username,password,database)

sql_queue = Queue.Queue()

def StartFingerprinting():
	banner_conf = open("conf/bannergrabbing.txt","r")
	keyword = []
	data = banner_conf.readline()
	while data:
		keyword.append(data.strip("\n"))
		data = banner_conf.readline()

	cursor = db.cursor()	
	host = get_hostdata()	
	print "[$]Start the p0f capturing"
	path = raw_input("[$]Enter the path of the packet capture:")
	clear(0)
	file_path = open(path,"r")
	loop=0
	while loop < len(host):
		data = host[loop].split("::")
		domain = data[0]
		ip = data[1]
		print "[$]Domain: "+domain
		cmd = "curl --connect-timeout 5 -I -k --location --max-redirs 5 '"+domain+"'"
		clear(0)
		status, output = commands.getstatusoutput(cmd)
		http_data = output.split("\n")
		tuple_v=""
		value=""
		k_loop = 0
		while k_loop < len(keyword):
			t1 = keyword[k_loop].split("@")
			p1 = t1[0]
			p1_val = t1[1].split("##")
			present = False
			h_loop = 2 # First three lines of curl is not required
			while h_loop < len(http_data):
				p_loop = 0
				while p_loop < len(p1_val):
					#print p1_val[p_loop]
					#print http_data[h_loop]
					if p1_val[p_loop].strip("\n") in http_data[h_loop]:
						present = True
						temp = http_data[h_loop].lstrip(p1_val[p_loop].strip("\n")+" ")
						value += ": :'"+temp.strip("\r\n")+"'"
						break
					p_loop+=1	
				h_loop+=1
			if not present:
				value += "'Not-Available'"
			tuple_v += p1+","
			value += ","
			k_loop+=1
		value = (value.strip(": :")).replace("': :'",": :")
		value = value.replace(",: :",",")
		tuple_v = tuple_v.replace("-","")
		tuple_v = "Domain, IP, OperatingSystem, "+tuple_v
		file_path = open(path,"r")
		os_data = file_path.readline()
		while os_data:
			if "syn+ack" in os_data and ip in os_data:
				suf_data = "'"+domain+"', '"+ip+"', '"+os_data[os_data.find("|os=")+4:os_data.find("|dist=")]+"'"
				break
			else:
				suf_data = "'"+domain+"', '"+ip+"', '"+"Not-Available"+"'"
			os_data = file_path.readline()
		file_path.close()
		value = suf_data+","+value	
		sql = "insert into http_response ("+tuple_v.strip(",")+") values ("+value.strip(",")+")"
		try:
			cursor.execute(sql)
			print "[$]Inserting http data for domain : "+domain
			time.sleep(2)
			clear(0)
			db.commit()
		except Exception:
			print "[*]Error interting query for domain : "+domain
			time.sleep(2)
			clear(0)
			loop+=1

def get_hostdata(): 	
	host = []
	cursor = db.cursor()
	cursor.execute("select * from domain2host")
	data =  cursor.fetchall()
	for row in data:
		host.append(row[0]+"::"+row[1])
	return host
