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
import time
import MySQLdb
import Queue
import thread
import threading
import urllib
from subroutines import *

db = MySQLdb.connect(host,username,password,database)
lock=thread.allocate_lock()
q_wget_url = Queue.Queue()
exif_queue = Queue.Queue()
exif_list = []

def get_exifkeyword():
	r_keyword=open("conf/exifconf.txt","r")
	exif_data=""
	exif_string=r_keyword.readline()
	while exif_string:
		exif_list.append(exif_string.strip("\n"))
		exif_data=exif_data+exif_string.strip("\n")	
		exif_data+="::Not-Available##"
		exif_string=r_keyword.readline()
 	return exif_data

'''def get_filetype():
	r_filetype=open("conf/file_type.txt","r")
	file_type = []
	extension = r_filetype.readline()
	while extension:
		file_type.append(extension)
		extension = r_filetype.readline()
	return file_type

def check_file(filename,file_type):
	loop = 0
	while loop < len(file_type):
		if file_type[loop].strip("\n") in filename.strip("\n"):
			return True
		loop+=1
	return False'''

def push_data(url):
	cmd="wget --timeout=60 "+url.strip("\n")+" -P data/"
	q_wget_url.put(cmd)

def extract_data(q_wget_url,exif_data):
	queue_full = True
	while queue_full:
		try:
			#print "Queue_Size: "+str(q_wget_url.qsize())
			cmd = q_wget_url.get(False)
			#print "[$]Executing command: "+cmd
			exif_value = exif_data
			#try:	
			status, output=commands.getstatusoutput(cmd)
			#clear(0)
			if not status:
				url = cmd[cmd.find("wget --timeout=60 ")+18:cmd.find("-P ")]
				data=cmd.split(" ")
				file_name = urllib.unquote(data[2][data[2].rfind("/")+1:])
				print "[$]Downloaded File : "+file_name
				time.sleep(1)
				clear(0)
				cmd_extract = "exiftool -sort data/'"+file_name+"'"
				status_e, output=commands.getstatusoutput(cmd_extract)
				if not status_e:
					temp_list=output.split("\n")
					p=0
					while p < len(temp_list):	
						q=0
						while q < len(exif_list):
							if exif_list[q] in temp_list[p]:
								temp_value = temp_list[p].split(":",1)
								parameter = temp_value[0].rstrip(" ")
								value = (temp_value[1].rstrip("\n")).strip(" ")
								exif_value = exif_value.replace(parameter+"::Not-Available",parameter+"::"+value)
								break
							q+=1
						p+=1
					#lock.acquire()
					exif_queue.put("Url::"+url+"##"+exif_value)
					#lock.release() #lock released
					print "[$]Exif Queue: "+str(exif_queue.qsize())
					sys.stdout.write("\033[F")
					sys.stdout.write("\033[K")	
				else:
					print "[*]Error while running the below command :"
					print "[*]"+cmd_extract+"\n"
					time.sleep(2)
					clear(0)
					clear(0)
				
			#except:
			else:
				print "[*]Error while running command :"
				#print "[*]"+cmd+"\n"
				time.sleep(2)
				clear(0)
		except Queue.Empty:
			queue_full = False 

def startextraction(q_wget_url,exif_data):
	t = []
	thread_count=20
        for i in range(thread_count):
             t.append(threading.Thread(target=extract_data, args=(q_wget_url,exif_data, )))
             t[i].start()
	     	
	loop=0
	while True:
		 if t[loop].isAlive():
		 	time.sleep(1)
			loop=0
		 else:
		 	loop+=1
		 if loop >= thread_count:
			break
def dataextractor():
	r_file=open("output/uri_list.txt","r")
	exif_data=get_exifkeyword()
	file_type=get_filetype()
	url = r_file.readline()
	while url:
		filename = url[url.rfind("/")+1:-1]
		match = check_file(filename,file_type)
		if match:
			push_data(url)
		
		'''else:
			print "Url :"+url+" does not seems to have valid file format"'''
		url = r_file.readline()
	startextraction(q_wget_url,exif_data)
	print "-----------------------------------------"
	time.sleep(2)
	clear(0)
	data =  exif_queue.get()	
	while True:
		rows=""
		values=""
		temp_tuple = (data.rstrip("#")).split("##")
		m=0
		while m < len(temp_tuple):
			#print temp_tuple[m]
			val = temp_tuple[m].split("::")
			rows+=val[0]+","
			if val[1]:
				values+="'"+val[1]+"',"
			else:
			    values+="'Not-Available',"	
			m+=1
		rows=rows.replace(" ","")
		rows=rows.replace("-","")
		cursor = db.cursor()
                print "[$]Inserting Doc Metadata"
		time.sleep(1)
		clear(0)
                sql = "insert into docmetadata ("+rows.strip(",")+") values ("+values.strip(",")+")"
		#print sql
		try:	
                	cursor.execute(sql)
		except Exception:
			print "Below query does not execute successfully"
			clear(0)
			#print sql
                db.commit()
		try:	
			data =  exif_queue.get(False)
		except Queue.Empty:
			print "Data processing completed"
			time.sleep(5)
			clear(0)
			break	
