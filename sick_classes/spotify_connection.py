""" Connect to Spotify API """

import json
import base64
import random
import requests
import re

class SpotifyConnection:

	def __init__(self):
		with open('../spotify_credentials.json') as credentials:
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

	def search(self, query):
		payload = {'q':query, 'type':'artist,album', 'limit':'15', 'market':'GB'}
		results = self.make_request('search', payload)
		#html = str(results)
		html = ''
		#for artist in results['artists']['items']:
		#	html+=self.preview(artist)
		html+=self.preview(results['artists']['items'][0])
		for album in results['albums']['items']:
			html+=self.preview(album)
		return html

	def preview(self, item):
		red = random.randint(150, 255)
		green = random.randint(30, 50)
		blue = random.randint(30, 50)
		tranlucence = (random.randint(35,55))/100
		pretty_url = f"/{item['type']}s/"+re.sub('[^a-zA-Z\d-]', '-', item['name']).lower()
		full_url = f"{pretty_url}/{item['id']}"
		try:
			release_year = " ("+item['release_date'].split('-')[0]+")"
		except:
			release_year = ''

		try:
			cover_image = item['images'][1]['url']
		except IndexError:
			try:
				cover_image = item['images'][0]['url']
			except IndexError:
				cover_image = ''

		preview = f"""
			<div class="preview" id="preview_{item['id']}" data-resource-url='{item['href']}' data-full-url='{full_url}' data-title='{item['name']}' data-pretty-url='{pretty_url}'>
				<h2>{item['name']} {release_year}</h2>
				<div class="image" style='background-image: url("{cover_image}")'></div>
				<div class="overlay" style="background:rgba({red},{green},{blue},{tranlucence})"></div>
			</div>
		"""
		return preview