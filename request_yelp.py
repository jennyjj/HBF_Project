import requests
import os
import json
import pprint
from random import choice

def get_restaurant(location):

	token_url = 'https://api.yelp.com/oauth2/token'

	payload = { 'grant_type': 'client_credentials',
	        'client_id': os.environ['YELP_CLIENT_ID'].rstrip(), 
	        'client_secret': os.environ['YELP_CLIENT_SECRET'].rstrip()}
	print payload

	response = requests.post(token_url, data=payload)
	if response.status_code != 200:
		print "Error Status {} - {}".format(response.status_code, response.reason)
		return;

	token = response.json()
	print response

	access_token = token['access_token']
	headers = {'Authorization': 'Bearer ' + access_token} # authentication information will be in header


	params = dict(term='restaurants', location=location, radius=40000) # search conditions

	response = ""
	while response == "":
		try:
			response = requests.get('https://api.yelp.com/v3/businesses/search',
		            params=params,
	    	        headers=headers) # get businesses from keyword search
		except:
			time.sleep(5)
			continue

	result = response.json()
	print result

	result_chosen = choice(result['businesses'])

	i = 0
	while result_chosen['coordinates']['latitude'] == None or result_chosen['coordinates']['longitude'] == None and i < 10:
		result_chosen = choice(result['businesses'])
		i += 1	

	if result_chosen['coordinates']['latitude'] == None or result_chosen['coordinates']['longitude'] == None:
		result_chosen['coordinates']['latitude'] = 0
		result_chosen['coordinates']['longitude'] = 0

	result_chosen_id = result_chosen['id']
	result_chosen_name = result_chosen['name']
	result_chosen_location = result_chosen['location']['display_address'][0]
	result_chosen_location2 = result_chosen['location']['display_address'][1]
	result_chosen_coordinates = result_chosen['coordinates']
	result_chosen_image = result_chosen['image_url']

	return [result_chosen_id, result_chosen_name, result_chosen_location, result_chosen_location2, result_chosen_coordinates, result_chosen_image]
