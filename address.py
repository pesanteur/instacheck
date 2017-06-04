import json
import requests

API_KEY = '<<INSERT API KEY HERE>>' # API_KEY from google maps here
url = 'https://maps.googleapis.com/maps/api/geocode/json?address='

def find_address(name):
	api_call = url + name + '&key='+ API_KEY
	response = requests.get(api_call)
	json_data = json.loads(response.text)
	latitude = json_data['results'][0]['geometry']['location']['lat']
	longitude = json_data['results'][0]['geometry']['location']['lng']
	long_name = json_data['results'][0]['address_components'][0]['long_name']
	short_name = json_data['results'][0]['address_components'][0]['short_name']
	return latitude, longitude, long_name, short_name
	
		
