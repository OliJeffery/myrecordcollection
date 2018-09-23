""" Connect to Spotify API """

import json
import base64
from urllib import parse
import requests
from flask import Flask,redirect

class SpotifyConnection:

	def __init__(self):
		with open('../sick_credentials/spotify_credentials.json') as credentials:
			json_credentials = json.loads(credentials.read())
			#self.auth = str(base64.b64encode(bytes(json_credentials['client_id']+':'+json_credentials['client_secret'], 'utf-8'))).split("'")[1]
			self.client_id = json_credentials['client_id']
			self.client_secret = json_credentials['client_secret']
			self.accounts_url = 'https://accounts.spotify.com/api/'
			self.base_url = 'https://api.spotify.com/v1/'
			self.token = self.get_token()

	def get_token(self):
		body_params = {'grant_type' : 'client_credentials'}
		url = self.accounts_url+'token'
		response=requests.post(url, data=body_params, auth = (self.client_id, self.client_secret))
		return response.json()['access_token']

	def make_request(self, request, params=None):
		url = self.base_url+request
		headers = {'Authorization':f'Bearer {self.token}'}
		response = requests.get(url,headers=headers,params=params)
		return response.json()

	def redirect_to(self, url):
		return redirect(url, code=302)

	def query_string(self, string):
		return parse.urlencode(string)

	def post_request(self, url, body_params):
		response=requests.post(url, data=body_params, auth = (self.client_id, self.client_secret))
		return response.json()
