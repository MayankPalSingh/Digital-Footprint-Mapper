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
import string
import re
import nltk
from nltk.sem import relextract
from string import join
from urllib import urlopen
import MySQLdb
import webarticle2text
from subroutines import *

db = MySQLdb.connect(host,username,password,database)
cursor=db.cursor()


def update_db(url,objsym,subjsym,lcon,filler,rcon):
	print url.strip("\n")
	time.sleep(1)
	clear(0)
	sql = "insert into data_analysis(Url, Object, Subject, Entity1, Filler, Entity2) values ('%(url)s','%(objsym)s','%(subjsym)s','%(lcon)s','%(filler)s','%(rcon)s')" % vars()
	try:
		#print sql
		#time.sleep(1)
		#clear(0)	
		cursor.execute(sql)
		#print "[$] Updating Database"
		db.commit()
	except Exception:
		print "[$]Error Updating Database"
		time.sleep(2)
		clear(0)	


def removeNonAscii(s): 
	return "".join(i for i in s if ord(i)<128)

def startanalyzing():
	file_path=open("output/uri_list.txt","r")
	url = file_path.readline()
	while url:	

		try:
			data = webarticle2text.extractFromURL(url)
		except Exception:
			#print "[$]Unable to fetch url :"+url	
			time.sleep(2)
			#clear(0)	
			
		text = nltk.word_tokenize(data)
		tagged_data = nltk.pos_tag(text)

		grammar = "NP: {<DT>?<JJ>*<NN>}"

		cp = nltk.RegexpParser(grammar)
		result_tree=cp.parse(tagged_data)

		pairs = relextract.mk_pairs(result_tree)

		reldicts = relextract.mk_reldicts(pairs)
		
		loop=0
		while loop < len(reldicts):
			for k,v in reldicts[loop].items():
			     #print k, '=>', v
			     if k == "objsym":
					objsym = v
					objsym=removeNonAscii(objsym)
			     if k == "subjsym":
					subjsym = v
					subjsym=removeNonAscii(subjsym)
			     if k == "lcon":
					lcon = v
					lcon = ((re.sub('/[A-Z]+','',lcon)).replace(",/,","")).replace("'","")	
					lcon=removeNonAscii(lcon)
			     if k == "filler":
					filler = v
					filler = ((re.sub('/[A-Z]+','',filler)).replace(",/,","")).replace("'","")	
					filler=removeNonAscii(filler)
			     if k == "rcon":
					rcon = v
					rcon = ((re.sub('/[A-Z]+','',rcon)).replace(",/,","")).replace("'","")
					rcon=removeNonAscii(rcon)
			if len(subjsym) > 4 and len(lcon) > 4 and len(rcon) > 4 and len(filler) > 4:
			    update_db(url,objsym,subjsym,lcon,filler,rcon)
			loop+=1
		url = file_path.readline()

