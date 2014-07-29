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
import commands
import urllib2
import requests
import MySQLdb
from BeautifulSoup import BeautifulSoup
from variables import *

host=" "
username=" "
password=" "
database=" "
def dbconf():
	global host
	global username
	global password
	global database
	dbfile=open("conf/database.txt","r")
        host=(((dbfile.readline()).strip("\n")).split(":"))[1]
        username=(((dbfile.readline()).strip("\n")).split(":"))[1]
        password=(((dbfile.readline()).strip("\n")).split(":"))[1]
        database=(((dbfile.readline()).strip("\n")).split(":"))[1]


dbconf()

db = MySQLdb.connect(host,username,password,database)
cursor = db.cursor()

value = ""

def clear(val):
        if val==0:
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
        if val==1:
                sys.stdout.write("\033[F")
        if val==2:
                sys.stdout.write("\033[K")


def insert_domain(url):
	if "https://" in url:
		url=url[url.find("https://")+8:url.find("/",-1)]
	elif "http://" in url:
		url=url[url.find("http://")+7:url.find("/",-1)]
	if "/" in url:
		temp=url.split("/")
		domain.append(temp[0])
		print "[$]"+temp[0]
	else:
		domain.append(url)
		print "[$]"+url

def print_uniq_domain_uri():
	print "\n[$]"+str(len(set(domain)))+" unique domains identified"
	print "[$]"+str(len(set(uri)))+" unique uris identified"
	time.sleep(5)
	clear(0)
	clear(0)
	clear(0)

def writedomain(uritype="normal"):
	global domain_set
	Name = get_Name()
	if uritype=="dork":
		domainfile = open("output/dorkdomain_list.txt","w")
		urifile = open("output/dorkuri_list.txt","w")
	elif uritype=="analyze":
		domainfile = open("output/domain_list.txt","w")
		s_domainfile = open("output/temp_searched_domain_list.txt","w")
	elif uritype=="combine":
		domainfile = open("output/domain_list.txt","w")
	else:
		domainfile = open("output/temp_domain_list.txt","w")
		urifile = open("output/uri_list.txt","w")
		s_domainfile = open("output/temp_searched_domain_list.txt","w")
		s_urifile = open("output/searched_uri_list.txt","w")
	domain_set=list(set(domain))
	uri_set=list(set(uri))
	loop=0
	while loop < len(domain_set):
		if (Name.lower() in (domain_set[loop]).lower()) or (uritype=="combine"):
			domainfile.write(domain_set[loop]+"\n")
		elif uritype=="dork":
			domainfile.write(domain_set[loop]+"\n")
		else:
			s_domainfile.write(domain_set[loop]+"\n")
			
		loop+=1
	loop=0
	while loop < len(uri_set) and uritype != "analyze" and uritype != "combine":
		if Name.lower() in ((uri_set[loop])[uri_set[loop].find("://")+3:uri_set[loop].find("/", 11)]).lower():
			urifile.write(uri_set[loop]+"\n")
		elif uritype=="dork":
			urifile.write(uri_set[loop]+"\n")
		else:
			s_urifile.write(uri_set[loop]+"\n")
		loop+=1

def get_domainlist():
	return len(domain_set)

def get_domainval(val):
	return domain_set[val]

def initialize_domain(filetype="specific"):
	global domain_set
	domain_set=[]

	if filetype == "final":
		temp = open("output/domain_list.txt","r")
	elif filetype == "specific":
		temp = open("output/temp_domain_list.txt","r")
	elif filetype == "searched":
		temp = open("output/temp_searched_domain_list.txt","r")

	domain_list=temp.readlines()
	loop=0
	while loop < len(domain_list):
		domain_set.append(domain_list[loop].strip("\n"))		
		loop+=1

def input_Name():
	global name
	name = raw_input ("Enter the organization's name:")
	return name

def get_Name():
	return name

def get_filetype():
        r_filetype=open("conf/file_type.txt","r")
        file_type = []
        extension = r_filetype.readline()
        while extension:
                file_type.append(extension)
                extension = r_filetype.readline()
        return file_type

def get_technologytype():
        r_technologytype=open("conf/technology_type.txt","r")
        technology_type = []
        extension = r_technologytype.readline()
        while extension:
                technology_type.append(extension)
                extension = r_technologytype.readline()
        return technology_type

def check_file(filename,ext_type,techid=0):
        loop = 0
        while loop < len(ext_type):
                if (ext_type[loop].strip("\n") in filename.strip("\n")) and (not "doc" in filename.strip("\n")):
			if techid==0:
                        	return True
			else:
				return (ext_type[loop].strip("\n")).lstrip(".")	
                loop+=1
        return False

def analyze_searched_domain(type_search):
	global value
	initialize_domain(type_search)
	loop=0;
	while loop < get_domainlist():
		value = "DOMAIN#CERT_CHECK::VALUE#WEB_CHECK::VALUE#WHOIS_CHECK::VALUE"
		value = value.replace("DOMAIN#",get_domainval(loop)+"#")
		status_cer_check = check_certificate(get_domainval(loop))
		if status_cer_check == "error":
			value = value.replace("CERT_CHECK::VALUE","CERT_CHECK::Error")
			web_whois_check(loop)
		elif status_cer_check == "matched":
			value = value.replace("CERT_CHECK::VALUE","CERT_CHECK::Match")
			domain.append(get_domainval(loop))
		elif status_cer_check == "completed":
			web_whois_check(loop)
			value = value.replace("CERT_CHECK::VALUE","CERT_CHECK::Did not match")
		loop+=1
		updatedb(value)	

def updatedb(sql_value):
	sql_value = sql_value.replace("VALUE","Not checked")
	temp = sql_value.split("#")
	temp_domain = temp[0]	
	temp_cert = ((temp[1]).split("::"))[1]	
	temp_web = ((temp[2]).split("::"))[1]	
	temp_whois = (((temp[3]).split("::"))[1]).strip("\n")
	sql = "insert into domain_validation (Domain, CertCheck, WebCheck, WhoisCheck) value ('%(temp_domain)s','%(temp_cert)s','%(temp_web)s','%(temp_whois)s')" % vars()
	print "[$]Inserting domain validation stats for "+temp_domain
	clear(0)
	try:
		cursor.execute(sql)
		db.commit()
	except Exception:
		print "[*]Error inserting into database "+temp_domain
		clear(0)
		
def web_whois_check(loop):
	global value
	status_web_check = check_website(get_domainval(loop))
	if status_web_check == "error":
		value = value.replace("WEB_CHECK::VALUE","WEB_CHECK::Error")
		status_whois = check_whois(get_domainval(loop))
		if status_whois == "whois error":
			value = value.replace("WHOIS_CHECK::VALUE","WHOIS_CHECK::Validation incomplete")
		elif status_whois == "whois match":
			value = value.replace("WHOIS_CHECK::VALUE","WHOIS_CHECK::Match")
			domain.append(get_domainval(loop))
		elif status_whois == "whois completed":
			value = value.replace("WHOIS_CHECK::VALUE","WHOIS_CHECK::Did not match")
	elif status_web_check == "matched":
		value = value.replace("WEB_CHECK::VALUE","WEB_CHECK::Match")
		domain.append(get_domainval(loop))
	elif status_web_check == "completed":
		value = value.replace("WEB_CHECK::VALUE","WEB_CHECK::Did not match")


def check_certificate(domain_name):
	cmd = "timeout 20 openssl s_client -connect "+domain_name+":443 2>/dev/null| openssl x509 -noout -subject"
	status, output = commands.getstatusoutput(cmd)
	data = output.split("\n")
	org_name=get_Name()+" "
	org_name_dot=get_Name()+"."
	loop = 0
	while loop < len(data):
		if "unable to load" in data[loop]:
			return "error"
		elif org_name_dot.lower() in data[loop].lower() or org_name_dot.lower() in data[loop].lower():
			return "matched"
		loop+=1
	return "completed"

def check_website(domain_name):
	temp_href = []
	web_key= open("conf/website_check.txt","r")
	keyword=(web_key.readlines())
	url = "http://"+domain_name
	try:
		html_page = urllib2.urlopen(url,timeout=10)
		#print html_page.read()
		soup = BeautifulSoup(html_page.read())
		for a in soup.findAll('a'):
			try:
				temp_href.append(a['href'])
				#print a['href']
			except Exception:
				checkme = "Error"
		status_check="error"
		loop = 0
		while loop < len(temp_href):
			k_loop = 0
			while k_loop < len(keyword):
				#keyword found in the web page
				if (keyword[k_loop].lower()).strip("\n") in temp_href[loop].lower():
					status_check = website_read(domain_name, temp_href[loop]) 
					if status_check == "matched":
						return status_check 	
				k_loop+=1	
			loop+=1
		return status_check
	except Exception:
		return "error"

def website_read(domain, link):
	org_name = get_Name()+" "
	if "http" in link:
		try:	
			html_page = requests.get(link,timeout=10)
		except Exception:
			return "error"
	else:
		try:
			html_page = requests.get("http://"+domain+link, timeout=10)
		except Exception:
			try:
				html_page = requests.get("https://"+domain+link)
			except Exception:
				return "error"
	
	if html_page.status_code == 404:
		return "error"	

	data = (html_page.text).split("\n")
	loop = 0
	while loop < len(data):
		if org_name.lower() in (data[loop]).lower():
			return "matched"
		loop+=1
	return "completed"			

def check_whois(domain):
	whoiserr = open("conf/whoiserror.txt","r")
	keywords = whoiserr.readlines()
	org_name = get_Name()+" "
	org_name1 = get_Name()+"."
	loop =  domain.count(".")
	error_check = ""
	while loop > 0:
		domain = domain[domain.find(".")+1:len(domain)] 
		cmd = "whois -H "+domain	
		status, output = commands.getstatusoutput(cmd)
		outdata = list(output.split("\n"))
		loopbreak_status_err=False	
		loopbreak_status_match=False	
		k=0
		while k < len(keywords):
			d=0
			while d < len(outdata):
				if (keywords[k].strip("\n")).lower() in  outdata[d].lower():
					loopbreak_status_err = True
					break
				elif (org_name in outdata[d].lower()) or (org_name1 in outdata[d].lower()) :
					loopbreak_status_match = True
					break
				d+=1
			if loopbreak_status_err:
				break	
			elif loopbreak_status_match:
				break	
			k+=1	
		if loopbreak_status_err:
			error_check = "whois error"
		elif loopbreak_status_match:
			return "whois match"
		else:
			return "whois completed"
		loop-=1
	return "whois error"
