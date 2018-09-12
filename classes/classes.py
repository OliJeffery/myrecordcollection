""" Gets a user token which we can use to make further requests """

import json
import requests
from decorators.decorators import html_page
from flask import url_for

class DiscogsConnection:
	"""Connects to the Discogs API"""
	def __init__(self):
		with open('credentials/credentials.json') as credentials:
			json_creds = json.loads(credentials.read())
			self.api_key = json_creds['api_key']
			self.api_secret = json_creds['api_secret']
			self.url_base = "https://api.discogs.com/"

	def search(self,search_str):
		params = {
			'q':search_str,
			'key':self.api_key,
			'secret':self.api_secret
		}
		url = f"{self.url_base}database/search"
		request = requests.get(url, params=params)
		if request.status_code == 200:
			try:
				pagination = request.json()['pagination']
				results = request.json()['results']
				if(len(results)>0):
					return(self.format_results(results))
				else:
					return "Couldn't find any results for that, sorry."
			except Exception as ex:
				print(ex)
				exit()
		else:
			print(request.status_code)

	def format_results(self, results):
		html = ''
		for result in results:
			if(result['type']=='artist'):
				artist = Artist(result)
				html+=artist.preview()
		return html

	@html_page
	def home(self):
		return "Hello world"


class Artist:
	"""Returns an artist object"""
	def __init__(self, artist):
		self.title = artist['title']
		self.id = artist['id']
		self.thumb = artist['thumb']
		self.uri = artist['uri']
		self.cover_image = image_from_url(artist['cover_image'], f'thumbnail_{self.id}', '/thumbnails/')
		self.resource_url = artist['resource_url']

	def preview(self):
		preview = f"""
			<div class="artist" id="artist_{self.id}">
				<h2>{self.title}</h2>
				<a href='{self.resource_url}'>
					<img src='/{self.cover_image}'>
				</a>
			</div>
		"""
		return preview

	def artist_profile(self):
		html = f"""
			<div class="artist" id="artist_{self.id}">
				<h2>{self.title}</h2>
				<a href='{self.resource_url}'>
					<img src='{self.cover_image}'>
				</a>
			</div>
		"""
		return html

def image_from_url(image_url, name, folder = '/'):
	"""Saves an image and writes it"""
	image_data = requests.get(image_url).content
	image_path = f'images{folder}{name}.jpg'
	with open(image_path, 'wb+') as saved_image:
		saved_image.write(image_data)
	return f'{image_path}'