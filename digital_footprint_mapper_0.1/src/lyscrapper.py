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
	loop=1
	while True:
		if "filetype" in query:
			sec = random.randint(1,30)
		else:	
			sec = random.randint(1,60)
		print "[*]Going to sleep for "+str(sec)+" seconds"
		time.sleep(sec)
		clear(0)	
		try:
			html_page = urllib2.urlopen("http://search.lycos.com/web?q="+query+"&keyvol=0079cb1589287ab9e5a3&pn="+str(loop))
			soup = BeautifulSoup(html_page.read())
			case = 0
			for link in soup.findAll('span', attrs={'class':'result-url'}):
				case += 1
				tmp = (((str(link)).strip("</span>")).split(">"))
				time.sleep(1)
				uri.append(tmp[1])
				insert_domain(tmp[1])	
				clear(0)
			if case <= 0:
				break
			loop+=1
		except Exception:
			print "Error while fetching url or probably searched might have been blocked.Sleep time 500 sec."
			time.sleep(500)

def lyscrapper():
	query_file = open("conf/generic_query.txt","r")
	query = query_file.readline()
	while query:
		query = query.replace(" ","+")
		print "[$]Executing query "+query.strip("\n")
		search_results(query.strip("\n"))
		clear(0)
		query = query_file.readline()
		
