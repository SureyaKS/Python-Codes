import pandas as pd
import smtplib
import urllib2
import json
import sys
import MySQLdb
import warnings
import pandas as pd
import time
import requests
import os
warnings.simplefilter(action = "ignore", category = FutureWarning)
warnings.simplefilter(action = "ignore", category = UserWarning)


def send_email():
	
	gmail_user = "yourMail@somemail.com"
	gmail_pwd = "YourpasswordGoesHere"
	
	FROM = gmail_user
	TO = [] #must be a list
	
	
	proceed = False

	temp = ""
	while ( temp != "*"):
		temp = raw_input("Enter the Mail Id, Press * to quit: ")
		if temp != '*' :
			TO.append(temp)
		print("Mail Id Received..")
	
	print "Mail id finalised."

	for ids in TO:
		if "@" not in ids or ".com" not in ids:
			print "The Mail id "+ids+" is not valid mail id."
			sys.exit()

	SUBJECT = raw_input("Enter the SUBJECT")
	print "\nEnter the Body of the mail.\n After you have typed Enter \"/done\" to finish"
	text = ""
	stopword = "/done"
	while True:
	    line = raw_input()
	    if line.strip() == stopword:
	        break
	    text += "%s\n" % line# Prepare actual message
	print "You have typed:\n"+text

	message = 'Subject: %s\n\n%s' % (SUBJECT, text)
	try:
		#server = smtplib.SMTP(SERVER) 
		server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
		server.ehlo()
		server.starttls()
		server.login(gmail_user, gmail_pwd)
		server.sendmail(FROM, TO, message)
		#server.quit()
		server.close()
		print 'successfully sent the mail'
		time_sent = time.asctime( time.localtime(time.time()) )
		update_mails(TO,SUBJECT,text,time_sent)
		finish_flag = True

		return finish_flag
	except Exception as exp:
		print "failed to send mail bcz of "+str(exp)
		finish_flag = False
		return finish_flag


def Is_Net_Working():

    url = 'http://www.google.com/'
    timeout=5
    try:
        _ = requests.get(url, timeout=timeout)
        return True
        
    except requests.ConnectionError:
    	return False



def Internet_functions():
	
    url = 'http://www.google.com/'
    timeout=5
    i =1
    try:

        while True :
            try:
                _ = requests.get(url, timeout=timeout)
                print "Connectivity Acquired again.."
                finish_flag = send_email()
                
                if finish_flag == True:
                	break
                elif finish_flag == False:
                	continue

                

             
            except requests.ConnectionError:
            	 

                print("No internet connection available. Next attempt after" + i+" secs")
                time.sleep(10*i)
            	
            
            except Exception as e:
            	#queue the proces that has to be.
                print "General Error occurred 1"
                break

    
    except Exception as e:
        print "General Error occurred 2"


if __name__ == "__main__":
	
	print "Checking the internet connectivity."

	net = Is_Net_Working()

	if net == True:
		print "Internet Works like a charm , Proceeding to Mail function."
		time.sleep(2)
		os.system('cls')
		send_email()

	elif net ==False:
		print "Internet Issues buddy."



