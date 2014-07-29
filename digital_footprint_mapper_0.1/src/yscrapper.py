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

import requests
from bs4 import BeautifulSoup
import time
import random
from variables import *
from subroutines import *

global domain
global uri
def search_yahoo(query,start,page):
        read=0
        while read <= 10:
                links = []
                pause = random.randint(1,30)
                print "[$]Going to sleep for "+str(pause)+" seconds"
                time.sleep(pause)
		clear(0)
                url = "http://in.search.yahoo.com/search?p=%s&b=%d&pstart=%d"
		try:
                	r = requests.get((url % (query, start, page)))
		except Exception:
			print "[*] Error while fetching url, probably search might have been blocked. Sleep 2700 sec."
			time.sleep(2700)
			
                soup=BeautifulSoup(r.text)
                a_list=soup.findAll('a')
		try:
                	links = [x.find('a')['href'] for x in soup.find('div', id='results').findAll('h3')]
		except Exception:
			print "[*] Error while fetching link"
			clear(0)
                loop = 0
                if len(links) < 1:
                        return True
                while loop < len(links):
			uri.append(links[loop])
			insert_domain(links[loop])
			time.sleep(1)
			clear(0)
                        loop+=1
                start+=10
                page+=1
                read+=1
def yscrapper():
	yfile_read=open("conf/generic_query.txt","r")
	query = yfile_read.readline()
	while query:
		print "[$]Executing query "+query.strip("\n")
		#query=query.lstrip("site:")
		start=1
		page=0
		while True:
			broke = search_yahoo(query,start,page)
			if broke:
				break
			if "filetype" in query:
				pause = random.randint(1,130)
			else:
				pause = random.randint(1,160)
			print "[$]Going to sleep for "+str(pause)
			time.sleep(pause)
			clear(0)
			start+=100
			page+=10
		clear(0)
		query = yfile_read.readline()
		


