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

#!/usr/bin/python2
import os
import sys
import signal
import time
from subroutines import *
import MySQLdb

db = MySQLdb.connect(host,username,password,database)

#Please set your api key here in between the qoute marks. 
userapi = "F0lRfjje0sUSUFcdMrDiCBiVAGzSUXJ2"
#yep right up there




try:
    from json       import dumps, loads
except:
    from simplejson import dumps, loads

try:
    # Python 2
    from urllib2    import urlopen
    from urllib     import urlencode
except:
    # Python 3
    from urllib.request     import urlopen
    from urllib.parse       import urlencode

__all__ = ['WebAPI']

class WebAPIError(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return self.value


class WebAPI:
    """Wrapper around the SHODAN webservices API"""
    
    class Exploits:
        
        def __init__(self, parent):
            self.parent = parent
            
        def search(self, query, sources=[], cve=None, osvdb=None, msb=None, bid=None):
            """Search the entire Shodan Exploits archive using the same query syntax
            as the website.
            
            Arguments:
            query    -- exploit search query; same syntax as website
            
            Optional arguments:
            sources  -- metasploit, cve, osvdb, exploitdb, or packetstorm
            cve      -- CVE identifier (ex. 2010-0432)
            osvdb    -- OSVDB identifier (ex. 11666)
            msb      -- Microsoft Security Bulletin ID (ex. MS05-030)
            bid      -- Bugtraq identifier (ex. 13951)
            
            """
            if sources:
                query += ' source:' + ','.join(sources)
            if cve:
                query += ' cve:%s' % (str(cve).strip())
            if osvdb:
                query += ' osvdb:%s' % (str(osvdb).strip())
            if msb:
                query += ' msb:%s' % (str(msb).strip())
            if bid:
                query += ' bid:%s' % (str(bid).strip())
            return self.parent._request('search_exploits', {'q': query})
    
    class ExploitDb:
        
        def __init__(self, parent):
            self.parent = parent
        
        def download(self, id):
            return self.parent._request('exploitdb/download', {'id': id})
        
        def search(self, query, **kwargs):
            return self.parent._request('exploitdb/search', dict(q=query, **kwargs))
    
    class Msf:
        
        def __init__(self, parent):
            self.parent = parent
            
        def download(self, id):
            return self.parent._request('msf/download', {'id': id})
        
        def search(self, query, **kwargs):
            return self.parent._request('msf/search', dict(q=query, **kwargs))
    
    def __init__(self, key):
        self.api_key = key
        self.base_url = 'http://www.shodanhq.com/api/'
        self.exploits = self.Exploits(self)
        self.exploitdb = self.ExploitDb(self)
        self.msf = self.Msf(self)
    
    def _request(self, function, params):
        # Add the API key parameter automatically
        params['key'] = self.api_key
        
        # Send the request
        data = urlopen(self.base_url + function + '?' + urlencode(params)).read().decode('utf-8')
        
        # Parse the text into JSON
        data = loads(data)
        
        # Raise an exception if an error occurred
        if data.get('error', None):
            raise WebAPIError(data['error'])
        
        # Return the data
        return data
    
    def count(self, query):
        return self._request('count', {'q': query})
    
    def locations(self, query):
        return self._request('locations', {'q': query})
    
    def fingerprint(self, banner):
        return self._request('fingerprint', {'banner': banner})
    
    def host(self, ip):
        return self._request('host', {'ip': ip})
    
    def info(self):
        return self._request('info', {})
    
    def search(self, query, page=1, limit=None, offset=None):
        args = {
            'q': query,
            'p': page,
        }
        if limit:
            args['l'] = limit
            if offset:
                args['o'] = offset
        
        return self._request('search', args)

def shodansearch():
	name=get_Name()
	#	exit()

	if userapi == "":
	    exit( 'You api key is not set. Please open the program and put your api key in the userapi variable.' )
	api = WebAPI(userapi)

	#settings all the variables for the program.
	arewescanmode = 'no'
	if arewescanmode != '--scan-mode':
	    shodansearch = name
	    shodantotal = 'y'
	    shodancountry = 'y'
	    shodanhostname = 'y'
	    shodanos = 'y'
	    shodanport = 'y'
	    shodanupdated = 'y'
	    shodandata = 'y'
	    shodanfileopt = 'y'
	elif arewescanmode == '--scan-mode':
	    shodansearch = raw_input( 'What would you like to search?:' )
	if arewescanmode != '--scan-mode':
	    if shodanfileopt == 'y':
		file_path = open("output/shodan-results.txt","w")
		shodanfile = "output/shodan-results.txt"
		while True:
		    if not os.path.exists(shodanfile):
			shodanfile = raw_input( 'File does not exist. Try again:' )
		    else:
			editshodanfile = open( shodanfile, 'w' )
			break

	#sets the initial try statement to grab all the results
	try:
	    # search shodan
	    results = api.search(shodansearch)

	    # show the results if not in scan mode
	    if arewescanmode != '--scan-mode':
		if shodansearch == 'y':
		    #print 'Results found: %s' % results['total']
		    if shodanfileopt == 'y':
			editshodanfile.write( 'Results found: %s\n' % results['total'] )
		for result in results['matches']:      
		    if shodanfileopt == 'y':
			editshodanfile.write( 'IP:: %s\n' % result['ip'] )
			if shodancountry == 'y':
			    editshodanfile.write( 'Country:: %s\n' % result['country_name'] )
			if shodanhostname == 'y':
			    editshodanfile.write( 'Hostname:: %s\n' % result['hostnames'] )
			if shodanos == 'y':
			    editshodanfile.write( 'OS:: %s\n' % result['os'] )
			if shodanport == 'y':
			    editshodanfile.write( 'Port:: %s\n' % result['port'] )
			if shodanupdated == 'y':
			    editshodanfile.write( 'Updated:: %s\n' % result['updated'] )
			if shodandata == 'y':
			    editshodanfile.write( '\n%s' % result['data'] )
	except Exception, e:
	    print 'Error: %s' % e
	#if in scan mode then this menu is used instead
	if arewescanmode == '--scan-mode':
	    
	    scanfileopt = raw_input( 'Would you like to save output to a file? [y/n]:' )
	    if scanfileopt == 'y':
		scanfile = raw_input( 'Please enter in the path to an existing file. This will overwrite it:' )
		while True:
		    if not os.path.exists(scanfile):
			scanfile = raw_input( 'File does not exist. Try again:' )
		    else:
			editshodanfile = open( scanfile, 'w' )
			tempscanfile = scanfile+'-temp'
			fin = open(tempscanfile, "r")
			break
	    os.system('clear')
	    #finds the estimated time
	    resultsinseconds = (results['total']*130)
	    if resultsinseconds >= 60 and resultsinseconds < 3600:
		estimatedtime = resultsinseconds/60
		print 'Estimated time to complete scanning all hosts: >%s minutes' % estimatedtime
	    elif resultsinseconds >= 3600 and resultsinseconds < 86400:
		estimatedtime = (resultsinseconds/60)/24
		print 'Estimated time to complete scanning all hosts: >%s days' % estimatedtime
	    elif resultsinseconds >= 86400 and resultsinseconds < 604800:
		estimatedtime = ((resultsinseconds/60)/24)/7
		print 'Estimated time to complete scanning all hosts: >%s weeks' % estimatedtime
	    elif resultsinseconds >= 604800 and resultsinseconds < 18144000:
		estimatedtime = (((resultsinseconds/60)/24)/7)/30
		print 'Estimated time to complete scanning all hosts: >%s months' % estimatedtime
	    elif resultsinseconds >= 18144000 and resultsinseconds < 217728000:
		estimatedtime = ((((resultsinseconds/60)/24)/7)/30)/12
		print 'Estimated time to complete scanning all hosts: >%s years' % estimatedtime
	    elif resultsinseconds > 217728000:
		print 'Estimated time to complete scanning all hosts: Unknown'
	     
	    #sets the menu and starts the scanning
	    def scanner(ignore):
		time.sleep(10)
	    def scannerfile(ignore):
		time.sleep(10)
	    for result in results['matches']:
		try:
		    print '#'*10+'Target Information'+'#'*10
		    print 'IP: %s' % result['ip']
		    print 'Country: %s' % result['country_name']
		    print 'Hostname: %s' % result['hostnames']
		    print 'OS: %s' % result['os']
		    print 'Updated: %s' % result['updated']
		    print '#'*10+'Nmap Output'+'#'*10
		    if scanfileopt != 'y':
			scanner('foo')
		    if scanfileopt == 'y':
			editshodanfile.write( '#'*10+'Target Information'+'#'*10+'\n' )
			editshodanfile.write( 'IP: %s\n' % result['ip'] )
			editshodanfile.write( 'Country: %s\n' % result['country_name'] )
			editshodanfile.write( 'Hostname: %s\n' % result['hostnames'] )
			editshodanfile.write( 'OS: %s\n' % result['os'] )
			editshodanfile.write( 'Updated: %s\n' % result['updated'] )
			editshodanfile.write( '#'*10+'Nmap Output'+'#'*10+'\n' )
			scannerfile('foo')
			editshodanfile.write( '\n' )
		except KeyboardInterrupt:
		    menuopt = raw_input( ':' )
		    if menuopt == 'rescan':
			if scanfileopt != 'y':
			    scanner( 'ignoring' )
			elif scanfileopt == 'y':
			    scannerfile( 'ignoring' )
		    elif menuopt == 'exit':
			if scanfileopt == 'y':
			    editshodanfile.close()
			    fin.close()
			print '\nExiting...'
			exit()
		    else:
			print 'Continuing...'
	    if scanfileopt == 'y':
		editshodanfile.close()
		fin.close()
	analyzeresult()


def analyzeresult():
	sresult = open("output/shodan-results.txt","r")
	
	sconf_list = initiate_sconf()

	data = sresult.readline()	
	while data:
		loop = 0
		while loop < len(sconf_list):
			mystring = sconf_list[loop]+':'
			if mystring in data:
				temp_data = data[data.find(mystring)+len(mystring)+1:data.find("\n",-1)]
				sconf_list[loop]+=":"+ temp_data
			loop+=1
		data = sresult.readline()
		if ("IP::" in data):
			update_db(sconf_list)
			sconf_list = initiate_sconf()
	

def initiate_sconf():
	sconf = open("conf/shodanconf.txt","r")
	sconf_list = []
	for line in sconf:
		sconf_list.append(line.strip("\n"))
	sconf.close()
	return sconf_list

def update_db(sconf_list):
	#print "inserting db"
	tuple_n = ""
	tuple_v = ""
	for keyword in sconf_list:
		if ":" in keyword:
			temp = keyword.split(":",1)
			tuple_n +=  temp[0]+","
			tuple_v +=  "'"+temp[1].replace("'","")+"',"
		else:
			tuple_n += keyword+","
			tuple_v += "'Not-Available'"+","	
	tuple_n = ((tuple_n.replace(" ","")).replace("-","")).strip(",")
	tuple_v = tuple_v.strip(",")
	cursor = db.cursor()
	sql = 	"insert into shodan_stat ("+tuple_n+") values ("+tuple_v+")"
	#print sql
	cursor.execute(sql)
	db.commit()

