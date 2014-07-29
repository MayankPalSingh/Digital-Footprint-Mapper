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

import urllib,urllib2
import time
import random
import sys
import torconn
from BeautifulSoup import BeautifulSoup
from variables import *
from subroutines import *

global domain
global uri
def bing_grab(query,start):
    address = "http://www.bing.com/search?q=%s&qs=n&filt=all&pq=%s&first=%d"
    address = address % (urllib.quote_plus(query),urllib.quote_plus(query),int(start))
    browse = random.randint(1,4)
    if browse == 1:
        request = urllib2.Request(address, None, {'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'} ) 
    elif browse == 2:
        request = urllib2.Request(address, None, {'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'} )
    elif browse == 3:
        request = urllib2.Request(address, None, {'User-Agent':'Mozilla/5.0'} )
    elif browse == 4:
        request = urllib2.Request(address, None, {'User-Agent':'Mozilla/5.10'} )

    try:	
    	urlfile = urllib2.urlopen(request)
    except Exception:
	print "[*] Error while fetching url, probably search has been blocked. Sleep 2700 sec"
	time.sleep(2700)
    #page=urlfile.read(200000)
    page=urlfile.read()
    #urlfile.close()

    soup = BeautifulSoup(page)
    if soup.find('div', id='results'):
	try:
    		links = [x.find('a')['href'] for x in soup.find('div', id='results').findAll('h3')]
	except Exception:
		print "[*] Error while fetching link"
		clear(0)
    	return links
    else:
	return "Empty"

def bscrapper():
    gfile = open("conf/generic_query.txt","r")
    query = gfile.readline() 	
    while query:
	    print "[*]Executing query "+query.strip("\n")	
	    start=10
	    while True:
		    links = bing_grab(query,start)
		    if links is "Empty":
			break
                    for i in range (len(links)):
			uri.append(links[i])
			insert_domain(links[i])
		    	time.sleep(1)
			clear(0)	
                    	i+=1
		    if start % 100 == 0:		
			    pause = random.randint(10,200)
			    print "[$]Going to sleep "+str(pause)
			    time.sleep(pause)
			    clear(0)
		    if "filetype" in query:		
			pause = random.randint(1,30)
		    else:	
			pause = random.randint(1,60)
		    print "[$]Going to sleep "+str(pause)
		    time.sleep(pause)
		    clear(0)	
		    start+=10
	    clear(0)	
            query=gfile.readline()
