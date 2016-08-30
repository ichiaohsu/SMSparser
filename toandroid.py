# -*- coding: utf8 -*-
from sys import exit
from datetime import datetime
import time

import csv
import sqlite3
import xml.etree.ElementTree as ET

class smsparser(object):

	def __init__(self):
		self.smses = list()
		self.dbname = 'smsdb.sqlite'
		print 'csvparser init...'

		conn = sqlite3.connect(self.dbname)
		cur = conn.cursor()
		cur.execute('''
		CREATE TABLE IF NOT EXISTS Contact (phone_number TEXT, thread_id INT)''')

	def checkphone(self,phonestr):
		if len(phonestr) == 10:
			print 'too short!'
			newphone = '+886' + phonestr[1:]
		else:
			newphone = phonestr
		return newphone

	def readcsv(self,csvname):
		print 'readcsv: ' + csvname
		if len(csvname) > 1:
			self.rf = open(csvname,'rb')
		else:
			print "invalid file name"
			exit(0)

	def parsecsv(self):

		for row in csv.DictReader(self.rf,["sms","type","rcv_number","snt_number","","date/time","group","message"]):

			# Decide message type
			if row["type"] == "deliver":
				phone_number = self.checkphone(row['rcv_number'])
				sms_type = '1'
			elif row["type"] == "submit":
				print row['snt_number']
				phone_number = self.checkphone(row['snt_number'])
				sms_type = '2'
			print phone_number

			# from csv string to datetime obj
			date_object = datetime.strptime(row["date/time"], '%Y.%m.%d %H:%M')
			#date_str = datetime.strftime(date_object,'%m月%d, %Y %H:%M')
			if date_object.hour > 12:
				date_str = datetime.strftime(date_object,'%Y年%m月%d日 下午%I:%M:00')
			else:
				date_str = datetime.strftime(date_object,'%Y年%m月%d日 上午%I:%M:00')
			print date_str

			# Create timestamp for sent time and receive time in ms
			sent_time = int( time.mktime( date_object.timetuple() ) )*1000
			receive_time = sent_time + 1000
			print "sent: ", sent_time, ", receive: ", receive_time

			print type(date_str)
			print type(row['date/time'])

			self.smses.append({
				'protocol': '0',
				'address': phone_number,
				'date': str(receive_time),
				'type': sms_type,
				'subject': 'null',
				'body': row['message'].decode('utf-8'),
				'toa': 'null',
				'sc_toa': 'null',
				'service_center': phone_number,
				'read': '1',
				'status': '-1',
				'locked': '0',
				'date_sent': str(sent_time),
				'readable_date': date_str.decode('utf-8'),
				'contact_name': '(Unknown)'
			})
		#print self.smses
			#thread_id = 295
			#data = [
			#	[date_str,phone_number,phone_number,msg_type,row["message"],str(thread_id),"null",str(sent_time),str(receive_time),
			#	0,1,-1,1,0,"null","+886932400860",0,1,0,0,"null",1,-1,0,"null", "466924201354160",0,0]
			#]

			#thread_id = thread_id + 1

	def convertxml(self):
		print 'convertxml...'
		xmlname = raw_input('Enter the desired xml output name - ')
		root = ET.Element('smses')

		for sms in self.smses:

			ET.SubElement(root,'sms', sms)
		tree = ET.ElementTree(root)
		# Add encoding parameter to indicate utf-8, solve encoding problem
		tree.write(xmlname, encoding='utf-8')
'''
def getData():
	print 'getData'
	input_name = raw_input("Enter file name to input - ")

	if len(input_name) > 1:
		rf = open(input_name,'rb')
	else:
		print "invalid file name"
		exit(0)

	output_name = raw_input("Enter file name for output - ")

	if len(output_name) > 1:

		wf = open(output_name,"w")
	else:
		print "Invalid output name. Use temp1.csv instead"

	# csv writer handler
	wdata = csv.writer(wf)

	# Write header for usage of SMS Backup and Restore app on android
	header = [
		["Date/Time","Number","Name","Type","Message","thread_id","person","date","date_sent","protocol",
		"read","status","type","reply_path_present","subject","service_center","locked","sub_id","phone_id"
		,"error_code","creator","seen","priority","group_id","si_or_id","imsi","block","spam"]
	]
	# Write header first
	wdata.writerows(header)


	thread_id = 295
	for row in csv.DictReader(rf,["sms","type","number","number2","error","date/time","group","message"]):

		# from csv string to datetime obj
		date_object = datetime.strptime(row["date/time"], '%Y.%m.%d %H:%M')
		date_str = datetime.strftime(date_object,'%m月%d, %Y %H:%M')

		print date_str

		# Create timestamp for sent time and receive time in ms
		sent_time = int( time.mktime( date_object.timetuple() ) )*1000
		receive_time = sent_time + 100
		print "sent: ", sent_time, ", receive: ", receive_time

		# Decide message type
		if row["type"] == "deliver":
			msg_type = "Received"
			phone_number = row["number"]
		elif row["type"] == "submit":
			msg_type = "Sent"
			phone_number = row["number2"]


		data = [
			[date_str,phone_number,phone_number,msg_type,row["message"],str(thread_id),"null",str(sent_time),str(receive_time),
			0,1,-1,1,0,"null","+886932400860",0,1,0,0,"null",1,-1,0,"null", "466924201354160",0,0]
		]

		thread_id = thread_id + 1

		wdata.writerows(data)
	rf.close()
	wf.close()
'''
