#! python3 
# login_gs.py - Authenticates Google Sheets to my specific Google Sheets account
# for instructions see quickstart.py at https://developers.google.com/sheets/api/quickstart/python
import gspread
import os
import httplib2
import logging 
import time 

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools 

from apiclient import errors

"""
try:
	elem = browser.find_element_by_id('location_search_location')
	print('Found <%s> element with that class name!' % elem.tag_name)
except:
	print('Was not able to find an element with that name.')
"""	

try:
	import argparse
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags = None
	
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json	

SCOPES = ['https://spreadsheets.google.com/feeds', 'https://docs.google.com/feeds']
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheet'

def get_credentials():
	""" Gets valid user credentials from storage.
	If nothing has been stored, or if the stored credentials are invalid, 
	the OAuth2 flow is completed to obtain the new credentials. 
	
	Returns: 
		Credentials, the obtained credential.
	"""
	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir, 
									'facebook_updater.json')
									
	store = oauth2client.file.Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		if flags:
			credentials = tools.run_flow(flow, store, flags)
		print ('Storing credentials to ' + credential_path)
	return credentials
	
def login():
	"""Tests basic usage of gspread.
	"""
	credentials = get_credentials()
	gc = gspread.authorize(credentials)
	return gc