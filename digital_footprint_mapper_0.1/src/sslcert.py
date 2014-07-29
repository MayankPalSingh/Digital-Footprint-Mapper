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
import commands	
from subroutines import *

db = MySQLdb.connect(host,username,password,database)
temp_list = []

def extract_sslcert_data():
	file_path=open("output/uri_list.txt","r")
	data =  file_path.readline()
	while data:
		if "https://" in data:
			domain = data[data.find("https://")+8:data.find("/",9)]
			temp_list.append(domain)
		data =  file_path.readline()
	ssl_list = list(set(temp_list))
	
	loop = 0 
	while loop < len(ssl_list):
		print "[$]Connect to domain: "+ssl_list[loop]
		ident = True
		if ":" in ssl_list[loop]:
			cmd1 = "echo | openssl s_client -connect "+ssl_list[loop]+" 2>/dev/null| openssl x509 -noout -dates"
			cmd2 = "echo | openssl s_client -connect "+ssl_list[loop]+" 2>/dev/null| openssl x509 -noout -issuer"
			cmd3 = "echo | openssl s_client -connect "+ssl_list[loop]+" 2>/dev/null| openssl x509 -noout -subject"
			cmd4 = "echo | openssl s_client -connect "+ssl_list[loop]+" 2>/dev/null| openssl x509 -noout -hash"
			cmd5 = "echo | openssl s_client -connect "+ssl_list[loop]+" 2>/dev/null| grep -i 'renegotiation'"
			cmd6 = "echo | openssl s_client -connect "+ssl_list[loop]+" 2>/dev/null| grep -i 'compression'"
			cmd7 = "echo | openssl s_client -connect "+ssl_list[loop]+" 2>/dev/null| openssl x509 -noout -fingerprint"
		else:
			cmd1 = "echo | openssl s_client -connect "+ssl_list[loop]+":443 2>/dev/null| openssl x509 -noout -dates"
			cmd2 = "echo | openssl s_client -connect "+ssl_list[loop]+":443 2>/dev/null| openssl x509 -noout -issuer"
			cmd3 = "echo | openssl s_client -connect "+ssl_list[loop]+":443 2>/dev/null| openssl x509 -noout -subject"
			cmd4 = "echo | openssl s_client -connect "+ssl_list[loop]+":443 2>/dev/null| openssl x509 -noout -hash"
			cmd5 = "echo | openssl s_client -connect "+ssl_list[loop]+":443 2>/dev/null| grep -i 'renegotiation'"
			cmd6 = "echo | openssl s_client -connect "+ssl_list[loop]+":443 2>/dev/null| grep -i 'compression'"
			cmd7 = "echo | openssl s_client -connect "+ssl_list[loop]+":443 2>/dev/null| openssl x509 -noout -fingerprint"

		status, output =  commands.getstatusoutput(cmd1)
		clear(0)
		if not status:
			temp = output.split("\n")
			notBefore =  temp[0]
			notAfter = temp [1]	
		else:
			ident = False
			#print "Unable to fecth certificate for domain "+ssl_list[loop]

		status, output =  commands.getstatusoutput(cmd2)
		if not status:
			issuer =  output
		else:
			ident = False
			#print "Unable to fecth certificate for domain "+ssl_list[loop]
		
		status, output =  commands.getstatusoutput(cmd3)
		if not status:
			subject =  output
		else:
			ident = False
			#print "Unable to fecth certificate for domain "+ssl_list[loop]
		
		status, output =  commands.getstatusoutput(cmd4)
		if not status:
			hash_val =  output
		else:
			ident = False
			#print "Unable to fecth certificate for domain "+ssl_list[loop]
			
		status, output =  commands.getstatusoutput(cmd5)
		if not status:
			renegotiation =  output
		else:
			ident = False
			#print "Unable to fecth certificate for domain "+ssl_list[loop]

		status, output =  commands.getstatusoutput(cmd6)
		if not status:
			compression =  output
		else:
			ident = False
			#print "Unable to fecth certificate for domain "+ssl_list[loop]
		
		status, output =  commands.getstatusoutput(cmd7)
		if not status:
			fingerprint =  output
		else:
			ident = False
			print "[*] Unable to fecth certificate for domain "+ssl_list[loop]
			time.sleep(2)
			clear(0)	
		
		cursor = db.cursor()
		if ident:
                	sql = "insert into sslstat (Domain, NotBefore, NotAfter, Issuer, Subject, Hash, Renegotiation, Compression, Fingerprint ) values ('"+ssl_list[loop]+"','"+notBefore+"','"+notAfter+"','"+issuer+"','"+subject+"','"+str(hash_val)+"','"+renegotiation+"','"+compression+"','"+fingerprint+"')"
                	print "Updating Database: "+ssl_list[loop]
			time.sleep(2)
			clear(0)	
               		try:
                        	cursor.execute(sql)
                	except Exception:
                        	print "[*] Error Updating Database"
				time.sleep(2)
				clear(0)	

                	db.commit()
		loop+=1
