import requests
import os
import json
import pprint
from random import choice

def get_restaurant(location):

	token_url = 'https://api.yelp.com/oauth2/token'

	payload = { 'grant_type': 'client_credentials',
            'client_id': os.environ['YELP_CLIENT_ID'][:-1], 
            'client_secret': os.environ['YELP_CLIENT_SECRET']}

	response = requests.post(token_url, data=payload)

	token = response.json()

	access_token = token['access_token']
	headers = {'Authorization': 'Bearer ' + access_token} # authentication information will be in header


	params = dict(term='restaurants', location=location, radius=40000) # search conditions

	response = requests.get('https://api.yelp.com/v3/businesses/search',
    	            params=params,
        	        headers=headers) # get businesses from keyword search

	result = response.json()

	result_chosen = choice(result['businesses'])

	result_chosen_name = result_chosen['name']
	result_chosen_location = result_chosen['location']['display_address'][0]
	result_chosen_location2 = result_chosen['location']['display_address'][1]

	return result_chosen_name, result_chosen_location, result_chosen_location2
