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
from subroutines import *

db = MySQLdb.connect(host,username,password,database)


def domain2url(dbtype="normal"):
	if dbtype == "dork":
		uri_read = open("output/dorkuri_list.txt","r")
	else:
		uri_read = open("output/uri_list.txt","r")
	url = uri_read.readline()
	while url:
		#print url
		#clear(0)
		if "http:" in url:	
			domain = url[url.find("http://")+7:url.find("/",7)]
			update_database(domain.strip(" "),url.strip("\n"),dbtype)
		if "https:" in url:
			domain = url[url.find("https://")+8:url.find("/",8)]
			update_database(domain.strip(" "),url.strip("\n"),dbtype)
		
		url = uri_read.readline()

def update_database(domain,url,dbtype):
        try:
                cursor = db.cursor()
		if dbtype == "dork":
			sql = "insert into dorkstat (domain,url) values ('%s','%s')" % (domain,url)
		else:
			sql = "insert into domain2url (domain,url) values ('%s','%s')" % (domain,url)
		#print sql
		time.sleep(2)
		#clear(0)
		cursor.execute(sql)
		db.commit()
        except:
                print "[$]Error while updating database !"
		time.sleep(2)
		clear(0)
                db.rollback()
