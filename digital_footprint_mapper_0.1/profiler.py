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



print "----------------------------------------------------------"
print "-                         DFMAP                          -"
print "-                       ---------                        -"
print "-                   Version 0.1, 2014                    -"
print "-                                                        -"
print "- Digital footprint mapper (DFMAP) is a tool to identify -"
print "- the footprints of the organization on the internet.    -"
print "- Digital footprints have critical piece of information  -"
print "- which can be leveraged by the cyber criminals.By using -"
print "- DFMAP one can get the overall picture of the           -"
print "- organization's digital footprints/internet presence.   -"
print "-                                                        -"
print "-               Author:Mayank Pal Singh                  -"
print "-               Email :mayankpalsingh74@gmail.com        -"
print "----------------------------------------------------------"
print
print

import sys
sys.path.insert(0,'src')
from variables import *
from subroutines import *
import gscrapper
import bscrapper
import yscrapper
import lyscrapper
import ascrapper
import time
import signal
import threading
import robtexextractor
import domain2host
import domain2url
import domainwhois
import ipwhois
import metadataextractor
import fingerprinting 
import techstat 
import sslcert
import dataanalysis
import shodan

print "Select the modules to execute :"
yscrp = raw_input("Enable Yahoo search engine scrapping [N]: ")
clear(0)
bscrp = raw_input("Enable Bing search engine scrapping [N]: ")
clear(0)
lscrp = raw_input("Enable Lycos search engine scrapping [N]: ")
clear(0)
ascrp = raw_input("Enable Ask search engine scrapping [N]: ")
clear(0)
robsrh = raw_input("Enable Robtex search of domains [N]: ")
clear(0)
domwho = raw_input("Enable whois on domain [N]: ")
clear(0)
ipwho = raw_input("Enable whois on ip [N]: ")
clear(0)
dataext = raw_input("Enable metadata extraction [N]: ")
clear(0)
finpri = raw_input("Enable fingerprinting [N]: ")
clear(0)
testta = raw_input("Enable techology stats [N]: ")
clear(0)
sslsta = raw_input("Enable SSL cert verification [N]: ")
clear(0)
datana = raw_input("Enable unstructured dataanalysis [N]: ")
clear(0)
dorsrh = raw_input("Enable Google dork search [N]: ")
clear(0)
sdnsrh = raw_input("Enable Shodan search [N]: ")
clear(0)
clear(0)

print "Following modules have been enabled:"
print "[+] Google Scrapping"
if yscrp=="y" or yscrp=="Y":
	print "[+] Yahoo Scrapping"
if bscrp=="y" or bscrp=="Y":
	print "[+] Bing Scrapping"
if lscrp=="y" or lscrp=="Y":
	print "[+] Lycos Scrapping"
if ascrp=="y" or ascrp=="Y":
	print "[+] Ask Scrapping"
if robsrh=="y" or robsrh=="Y":
	print "[+] Robtex Search"
if domwho=="y" or domwho=="Y":
	print "[+] Domain Whois"
if ipwho=="y" or ipwho=="Y":
	print "[+] IP Whois"
if dataext=="y" or dataext=="Y":
	print "[+] MetaData Extraction"
if finpri=="y" or finpri=="Y":
	print "[+] Fingerprinting"
if testta=="y" or testta=="Y":
	print "[+] Technology Statistics"
if sslsta=="y" or sslsta=="Y":
	print "[+] SSL statistics"
if datana=="y" or datana=="Y":
	print "[+] Unstructured Data Analysis"
if dorsrh=="y" or dorsrh=="Y":
	print "[+] Google Dork Search"
if sdnsrh=="y" or sdnsrh=="Y":
	print "[+] Shodan Search"


Name = input_Name()
clear(0)

def create_queries(Name,stype="normal"):
	while True:
		if not Name:
			print "Organization's name cannot be blank"
			time.sleep(2)
			clear(0)
			Name = input_Name()
			time.sleep(1)
			clear(0)
		elif "." in Name:
			sys.stdout.write( "Enter the name without specifying the TLD or SubDomains. For Example kpmg")
			raw_input () 
			clear(0)
			Name = input_Name()
			time.sleep(1)
			clear(0)
		else:
			createfile(Name,stype)
			print "\n[$]Search queries created for "+Name+" under conf directory"
			break

def createfile(Name, stype="normal"):
	if stype == "dork":
		gfile=open('conf/dquery.txt','w')
		query_file = open('conf/dorkqueries.txt','r')
	else:
		gfile=open('conf/gquery.txt','w')
		query_file = open('conf/queries.txt','r')
	query = query_file.readline()
	while query:
		gquery = query % vars()	
		gfile.write(gquery)		
		query = query_file.readline()

def create_generic_queries(Name):
	wquery = open("conf/generic_query.txt","w")
	tmp = (list(set(domain)))
	p = 0
	while p < len(tmp):
		query_file = open('conf/queries.txt','r')
		query = query_file.readline()
		while query:
			if Name.strip("\n") in tmp[p]:
				query=query.replace("%(Name)s","")
				query=query.replace("*","")
				query=query.replace("com","")
				query=query.replace(".","")
				query=query.replace("site:","site:"+tmp[p])
				wquery.write(query)		
			query = query_file.readline()
		p+=1

def sigint_handler(signum, frame):
	 print_uniq_domain_uri()
	 writedomain()
	 print "[*]Abrubt Termination : Domains and uris dumped in output directory"
	 sys.exit(1)


signal.signal(signal.SIGINT, sigint_handler)

print "\n[$]Extracting domain names from Google ..."
create_queries(Name)
gscrapper.gscrapper()
create_generic_queries(Name)
print "-------------------------------------"

if bscrp=="y" or bscrp=="Y":
	print "[$]Extracting domain names from Bing ... "
	bscrapper.bscrapper()
	print "-------------------------------------"

if yscrp=="y" or yscrp=="Y":
	print "[$]Extracting domain names from Yahoo ..."
	yscrapper.yscrapper()
	print "-------------------------------------"

if lscrp=="y" or lscrp=="Y":
	print "[$]Extracting domain names from Lycos ..."
	lyscrapper.lyscrapper()
	print "-------------------------------------"

if ascrp=="y" or ascrp=="Y":
	print "[$]Extracting domain names from Ask ..."
	ascrapper.ascrapper()
	print "-------------------------------------"

writedomain()

print "[$]Domain vaidation in progress ..."
analyze_searched_domain("searched")
analyze_searched_domain("specific")
writedomain("analyze")
print "-------------------------------------"


#print "Print domain -- profile"
#print get_domainlist()

if robsrh=="y" or robsrh=="Y":
	print "[$]Robtex search in progress ..."
	#Enable this function to initialize the domain list. If scrappers are hashed then enable this function.
	#initialize_domain("final")
	robtexextractor.robtex_extractor()
	print "-------------------------------------"

writedomain("combine")

print "[$]Domain to host mapping ..."
domain2host.domain2host()
print "-------------------------------------"

if domwho=="y" or domwho=="Y":
	print "[$]Whois on domain names ..."
	domainwhois.domainwhois()
	print "-------------------------------------"

if ipwho=="y" or ipwho=="Y":
	print "[$]Whois on ip addressess ..."
	ipwhois.ipwhois()
	print "-------------------------------------"

print "[$]Domain to url mapping, please wait...."
domain2url.domain2url()
print "-------------------------------------"

if dataext=="y" or dataext=="Y":
	print "[$]Meta data extraction ..."
	metadataextractor.dataextractor()
	print "-------------------------------------"

if finpri=="y" or finpri=="Y":
	print "[$]Fingerprinting ..."
	fingerprinting.StartFingerprinting()
	print "-------------------------------------"

if testta=="y" or testta=="Y":
	print "[$]Technology statistics ..."
	techstat.techstat()
	print "-------------------------------------"

if sslsta=="y" or sslsta=="Y":
	print "[$]SSL certificate validation ..."
	sslcert.extract_sslcert_data()
	print "-------------------------------------"

if datana=="y" or datana=="Y":
	print "[$]Unstructured data analysis ..."
	dataanalysis.startanalyzing()
	print "-------------------------------------"

if dorsrh=="y" or dorsrh=="Y":
	print "[$]Executing Google dork queries ..."
	create_queries(Name,"dork")
	gscrapper.gscrapper("dork")
	writedomain("dork")
	domain2url.domain2url("dork")
	print "-------------------------------------"

if sdnsrh=="y" or sdnsrh=="Y":
	print "[$]Shodan search ..."
	shodan.shodansearch()
	print "-------------------------------------"

