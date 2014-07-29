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

from BeautifulSoup import BeautifulSoup
import urllib2
import re
import mechanize
import time
import random
from variables import *
from subroutines import *

def search_results(query):
	prev_link = ""
	loop=1
	while True:
		if "filetype" in query:
			sec = random.randint(1,30)
		else:
			sec = random.randint(1,60)
		time.sleep(sec)
		print "[*] Going to sleep for "+str(sec)+" seconds"
		clear(0)
		try:
			html_page = urllib2.urlopen("http://www.ask.com/web?q="+query+"&page="+str(loop)+"&qid=86912AAAD2959E64589B3186E7BDD54C&qsrc=1&o=0&l=dir")
			soup = BeautifulSoup(html_page.read())
		except Exception:
			print "Error Fetching Url, search might have been blocked. Sleep 2700 sec"
			time.sleep(2700)
		case = 0
		for link in soup.findAll('div', attrs={'class':'wresult tsrc_tled'}):
			if link.a['href'] == prev_link:
                		break
            		if case == 0:
                		prev_link = link.a['href']
            		case+=1
		    	#print link.a['href']
			uri.append(link.a['href'])
			insert_domain(link.a['href'])
			clear(0)
			time.sleep(1) 	
		if case <= 0:
                	break	
		loop+=1

def ascrapper():
        query_file = open("conf/gquery.txt","r")
        query = query_file.readline()
        while query:
		query = query.replace(" ","+")
		print "[$]Executing query "+query.strip("\n")
                search_results(query.strip("\n"))
		clear(0)
                query = query_file.readline()

