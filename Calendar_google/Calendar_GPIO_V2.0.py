# -*- coding: utf-8 -*-
#Programe google calendar v2.0 7/02/2017
#programe exemple de google que j'ai modifier
#https://developers.google.com/google-apps/calendar/quickstart/python
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

#Biblioteque rajouter
import time
import RPi.GPIO as GPIO
from apscheduler.scheduler import Scheduler     #Relancement du programe sur basse temps
from feed.date.rfc3339 import tf_from_timestamp #comparateur obligatoir pour google
from pi_switch import RCSwitchSender            #Radio 433mhz



try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

#adresse du calendrier 
CALENDAR_ID = '2qr0loon4oee9ihgv3ktvtlc2s@group.calendar.google.com'
#Ficher d'acces au compte google
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

#Configuration Radio
sender = RCSwitchSender()
sender.enableTransmit(0)

#Configuration Sortie GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.OUT)
GPIO.output(25,GPIO.LOW)

#code Radio
code_on =12
code_off =11
#declaration variable sortie
out = 0


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    
   
    
    
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print (now)
    print('Getting the upcoming 1 events')
    eventsResult = service.events().list(
        calendarId=CALENDAR_ID , timeMin=now, maxResults=1, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
        GPIO.output(25,GPIO.LOW)
    for event in events:
		#debut de l'evenement 
        start = event['start'].get('dateTime', event['start'].get('date'))
		#fin de l'evenement
        end = event['end'].get('dateTime', event['end'].get('date'))
        #print(start, end, event['summary'])

        
        if time.strftime('%d-%m-%Y %H:%M',time.localtime(tf_from_timestamp(start))) <= time.strftime('%d-%m-%Y %H:%M') and time.strftime('%d-%m-%Y %H:%M') < time.strftime('%d-%m-%Y %H:%M',time.localtime(tf_from_timestamp(end))) :
            print("on")
            out = 1
            print (out)
        else:
            print("off")
            out = 0
            print(out)
                

        
        #gestion de la sortie
        if out == 1 :
            print ("GPIO")
            GPIO.output(25,GPIO.HIGH)
        else:
            GPIO.output(25,GPIO.LOW)


###############################################################################################
#            Fonction qui relance la lecture du fichier tout les 10 seconds                   #
###############################################################################################
def callable_func():
    get_credentials()
    print ("--------------main-------------")
    main()
    print ("-------------Sortie-------------")
  


#************************************************************************************# 
#****           Run scheduler service                                            ****#
#************************************************************************************# 
sched = Scheduler(standalone=True)
sched.add_interval_job(callable_func,seconds=5)
sched.start() 
