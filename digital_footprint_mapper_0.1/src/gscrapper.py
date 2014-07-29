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

import os
import sys
import time
import random
#import torconn 
from variables import *
from subroutines import *


global domain
global uri
if sys.version_info[0] > 2:
    from http.cookiejar import LWPCookieJar
    from urllib.request import Request, urlopen
    from urllib.parse import quote_plus, urlparse, parse_qs
else:
    from cookielib import LWPCookieJar
    from urllib import quote_plus
    from urllib2 import Request, urlopen
    from urlparse import urlparse, parse_qs

BeautifulSoup = None

url_home          = "http://www.google.%(tld)s/"
url_search        = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&btnG=Google+Search"
url_next_page     = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&start=%(start)d"
url_search_num    = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&num=%(num)d&btnG=Google+Search"
url_next_page_num = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&num=%(num)d&start=%(start)d"

home_folder = os.getenv('HOME')
if not home_folder:
    home_folder = os.getenv('USERHOME')
    if not home_folder:
        home_folder = '.'   # Use the current folder on error.
cookie_jar = LWPCookieJar(os.path.join(home_folder, '.google-cookie'))
try:
    cookie_jar.load()
except Exception:
    pass

def get_page(url):

	request = Request(url)
	browse=random.randint(1,8)
	if browse==1:
		request.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)')
	elif browse==2:		
		request.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')
	elif browse==3:		
		request.add_header('User-Agent','Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)')
	elif browse==4:		
		request.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1)')
	elif browse==5:		
		request.add_header('User-Agent','Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.1; AOLBuild 4334.5012; Windows NT 6.0; WOW64; Trident/5.0)')
	elif browse==6:		
		request.add_header('User-Agent','Opera/9.27 (X11; Linux i686; U; en)')
	elif browse==7:		
		request.add_header('User-Agent','Opera 9.4 (Windows NT 6.1; U; en)')
	elif browse==8:		
		request.add_header('User-Agent','Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/417.9 (KHTML, like Gecko) NetNewsWire/2.0')
	cookie_jar.add_cookie_header(request)
	response = urlopen(request)
	cookie_jar.extract_cookies(response, request)
	html = response.read()
	response.close()
	cookie_jar.save()
	return html

def filter_result(link):
	try:
		o = urlparse(link, 'http')
		if o.netloc and 'google' not in o.netloc:
	    		return link
		if link.startswith('/url?'):
		    link = parse_qs(o.query)['q'][0]

		    o = urlparse(link, 'http')
		    if o.netloc and 'google' not in o.netloc:
			return link
	except Exception:
		pass
	return None

def search(query, tld='com', lang='en', num=10, start=0, stop=None, pause=2.0):
    global BeautifulSoup
    if BeautifulSoup is None:
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            from BeautifulSoup import BeautifulSoup

    hashes = set()

    query = quote_plus(query)

    get_page(url_home % vars())

    if start:
        if num == 10:
            url = url_next_page % vars()
        else:
            url = url_next_page_num % vars()
    else:
        if num == 10:
            url = url_search % vars()
        else:
            url = url_search_num % vars()

    while not stop or start < stop:

        time.sleep(pause)
	
        html = get_page(url)

        soup = BeautifulSoup(html)
        anchors = soup.find(id='search').findAll('a')
        for a in anchors:

            try:
                link = a['href']
            except KeyError:
                continue

            link = filter_result(link)
            if not link:
                continue

            h = hash(link)
            if h in hashes:
                continue
            hashes.add(h)

            yield link

        if not soup.find(id='nav'):
            break

        start += num
        if num == 10:
            url = url_next_page % vars()
        else:
            url = url_next_page_num % vars()

def gscrapper(qtype="normal"):
	if qtype == "dork":
		gfile=open("conf/dquery.txt","r")
	else:
		gfile=open("conf/gquery.txt","r")
	query=gfile.readline()
	while query:
		print "[$]Executing query "+query.strip("\n")
		i=0;initiate=0;start=initiate;inactive=0
		k=0
		backup_url=""
		while True:
			clear(2)
			try:
				num=random.randint(1, 5)
				floatnum=num*random.random()
				url=""
				for url in search(query, num=100, start=initiate, stop=initiate+100, pause=floatnum):
					uri.append(url)
					insert_domain(url)
					time.sleep(1)
					clear(0)
					i+=1
			except Exception:
				print "[*] Google has identified you as a script. Search blocked :("
				print "[*] Sleep time 2700 seconds. Please hold on."
				time.sleep(2700)
				clear(0)
				clear(0)
			if ("filetype" in query) or (qtype == "dork"):		 
				number=random.randint(30, 100)
			else:
				number=random.randint(1, 400)
			print "[$]Going to sleep for "+str(number)+" seconds"
			clear(1)
			inactive=number
			time.sleep(inactive)
			initiate=i
			if backup_url==url:
				break
			else:
				backup_url=url
		clear(0)
		query=gfile.readline()
