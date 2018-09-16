""" Makes a connection to the Discogs api """

import json
import requests

class DiscogsConnection:

	"""Connects to the Discogs API"""
	def __init__(self, **kwargs):
		with open('credentials/credentials.json') as credentials:
			json_creds = json.loads(credentials.read())
			self.api_key = json_creds['api_key']
			self.api_secret = json_creds['api_secret']
			self.url_base = "https://api.discogs.com/"

	def get_resource(self, endpoint, params={}, authenticate = True, full_url=False):
		if(authenticate):
			params['key'] = self.api_key
			params['secret'] = self.api_secret
		if full_url:
			resource_url = endpoint
		else:
			resource_url = self.url_base+endpoint
		request = requests.get(resource_url, params=params)
		if request.status_code == 200:
			return request.json()
		else:
			return f"Failed on '{request.url}'."
