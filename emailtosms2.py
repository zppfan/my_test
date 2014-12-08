#!/usr/bin/env python^M
# -*- coding: utf-8 -*-^M
__author__ = u'sab'

import os,poplib,datetime,time
from RosAPI import Core

smsfile = "/home/sab/bin/emailtosms/numberofsmsout.txt"
with open(smsfile, 'r') as f:
  first_line_sms = f.readline()    
  second_line_date = f.readline()    
Mobile1="+7903650XXXX"
Mobile2="+7961616XXXX"
Mobile3="+7961616XXXX"
#sending sms at night only to 3
if (int(time.strftime("%H"))>7 and int(time.strftime("%H"))<23):
    smsreceivers=[Mobile1,Mobile2,Mobile3]
else:
    smsreceivers=[Mobile3]

print smsreceivers
numberofsmsout = int(first_line_sms)
print ("Today we send %s sms"%numberofsmsout)
print ("Date is %s "%second_line_date)
hostdude = "10.0.0.3"
server = "mail.XXXX.pro"
#port = 995
user = "smsalert"
passwd = "smsalert"
connect = False

pop = poplib.POP3(server)
pop.user(user)
pop.pass_(passwd)
arraysms = []
numMessages = len(pop.list()[1])
if numMessages < 5:
    for i in range(numMessages):
	for j in pop.retr(i+1)[1]:
#	    print "LINE IS %s"%j
	    if "Device " in j:		
		arraysms.append(j)#add email body to list of sms
else: arraysms = ['WARNING: More then 5 devices change status to down']
print arraysms
print ("we have %s messages to sms"%numMessages)
if numMessages>0:
    connect = True

poplist = pop.list()
if poplist[0].startswith('+OK') :
    msglist = poplist[1]
    for msgspec in msglist :
        # msgspec is something like "3 3941", 
        # msg number and size in octets
        msgnum = int(msgspec.split(' ')[0])
        print "Deleting msg %d\r" % msgnum
        pop.dele(msgnum)
    else :
        print "No messages for", user

else :
    print "Couldn't list messages: status", poplist[0]
pop.quit()
if connect:
    try:
	print("Connecting to Monitor server API")
        child = Core(hostdude)
    except:
        print('Host is unavailiable;please check /ip/services/api: %s'%host)
    else:
        user= "smsalert"
        password="smsalert"
        child.login(user,password)
        try:
	    for message in arraysms:
	        message=message+" SMStoday:%s"%numberofsmsout
		for abonent in smsreceivers:
    #		child.response_handler(child.talk(["/ip/service/set", "=disabled="+"yes", "=numbers="+"www"]))
		    print ("Sending message:%s to abonent:%s"%(message,abonent))
		    numberofsmsout+=1		    
            	    child.response_handler(child.talk(["/tool/sms/send","=port="+"usb3","=phone-number="+abonent, "=message="+message]))
	except:
    	    print('Login or command unsuccessful: %s'%hostdude)

#print "writing %s sms to file"%numberofsmsout
date = datetime.datetime.now().strftime("%Y%m%d")
f = open(smsfile, 'w')
if date == second_line_date:
    f.write('%d\n' % numberofsmsout)
else:
    f.write('0\n')
    print("New day! resetting sms count")
f.write(date)
f.close()