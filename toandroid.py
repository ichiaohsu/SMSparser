# -*- coding: utf8 -*-
import csv
from sys import exit
from datetime import datetime
import time

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
