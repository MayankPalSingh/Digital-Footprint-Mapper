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

import commands
import sys
import os
import random
import time
from variables import *
from subroutines import *
from bs4 import BeautifulSoup


def robtex_extractor():
	dlen = 0
	Name = get_Name()
	while dlen < get_domainlist():
		inactive=random.randint(1, 100)
		#print "In sleep mode for "+str(inactive)+" seconds"	
		#time.sleep(inactive)
		org = get_domainval(dlen)
		print "Feteching domains for "+org
		cmd="wget -P log/ https://www.robtex.com/dns/"+org+".html > log_file.txt 2>&1 "
		os.system(cmd)
		try:
			tempfile=open("log/"+org+".html","r")
			soup=BeautifulSoup(tempfile)
			a_list=soup.find_all('a')
		except Exception:
			print "File "+org+".html is not found"
			time.sleep(1)
			clear(0)
			clear(0)
		robtex_list=[]
		domain_list=[]
		domain_list.append(org)

		try:
			for anchor in soup.find_all('a'):
			    robtex_list.append(anchor.get('href', '/'))
		except Exception:
			print "[*] Error fetching url / Content Not Found"
			time.sleep(1)
			clear(0)
			clear(0)

		loop=0
		while loop < len(robtex_list):
			if "www.robtex.com/dns/" in robtex_list[loop]:
				value_domain=robtex_list[loop].split("/")
				extracted_value=(str(value_domain[4])).strip('html')
				name=org.split(".")
				if name[0] in extracted_value:
					if Name in extracted_value:
						print "++Extracting list for domain "+extracted_value
						time.sleep(1)
						clear(0)
						domain_list.append(extracted_value.strip('.'))
			loop+=1

		loop=0
		while loop < len(domain_list):
			if Name in domain_list[loop]:
				domain.append(domain_list[loop])
			loop+=1 
		clear(0)
		dlen+=1 
