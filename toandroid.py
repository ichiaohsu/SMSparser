# -*- coding: utf8 -*-
from sys import exit
from datetime import datetime
import time

import csv
import xml.etree.ElementTree as ET

class smsparser(object):

	def __init__(self):
		self.smses = list()
		print 'csvparser init...'

	def checkphone(self,phonestr):
		if len(phonestr) == 10:
			print 'too short!'
			newphone = '+886' + phonestr[1:]
		else:
			newphone = phonestr
		return newphone

	def readcsv(self):
		print 'readcsv...'

		csvname = raw_input("Enter file name to input - ")

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

			# from csv string to datetime obj
			date_object = datetime.strptime(row["date/time"], '%Y.%m.%d %H:%M')
			# Split into 12hour and Mandarin am/pm indication
			if date_object.hour > 12:
				date_str = datetime.strftime(date_object,'%Y年%m月%d日 下午%I:%M:00')
			else:
				date_str = datetime.strftime(date_object,'%Y年%m月%d日 上午%I:%M:00')

			# Create timestamp for sent time and receive time in ms
			sent_time = int( time.mktime( date_object.timetuple() ) )*1000
			receive_time = sent_time + 1000

			# Create entries for each sms
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

	def convertxml(self):
		print 'convertxml...'
		xmlname = raw_input('Enter the desired xml output name - ')

		root = ET.Element('smses')

		for sms in self.smses:

			ET.SubElement(root,'sms', sms)

		tree = ET.ElementTree(root)
		# Add encoding parameter to indicate utf-8, solve encoding problem
		tree.write(xmlname, encoding='utf-8')
