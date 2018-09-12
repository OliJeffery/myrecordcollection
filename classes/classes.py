""" Gets a user token which we can use to make further requests """

import json
from os import path
import requests
from decorators.decorators import html_page
from flask import url_for
from PIL import Image
import random

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
			item = DiscogItem(result)
			html+=item.preview()
		return html

	@html_page
	def home(self):
		return "Hello world"

class DiscogItem:

	def __init__(self, item):
		self.title = item['title']
		self.id = item['id']
		self.resource_url = item['resource_url']
		thumb_path = f'/images/thumbnails/thumbnail_{self.id}.jpg'
		if path.exists(thumb_path):
			# Uses an existing thumbnail if one exists
			self.thumbnail = thumb_path
		elif item['cover_image'] != 'https://img.discogs.com/images/spacer.gif':
			# Saves and uses a new thumbnail if none exits
			self.thumbnail = image_from_url(item['cover_image'], f'thumbnail_{self.id}', '/thumbnails/', True)
		else:
			self.thumbnail = '/images/thumbnails/holly_genero.jpg'

	def preview(self):
		red = random.randint(0, 255)
		green = random.randint(0, 255)
		blue = random.randint(0, 255)
		preview = f"""
			<div class="preview" id="artist_{self.id}">
				<h2>{self.title}</h2>
				<div class="image" style='background-image: url("{self.thumbnail}")'></div>
				<div class="overlay" style="background:rgba({red},{green},{blue},.25)"></div>
			</div>
		"""
		return preview

class Artist(DiscogItem):
	"""Returns an artist object"""


		
def image_from_url(image_url, name, folder = '/', thumbnail=False):
	"""Saves an image and writes it"""
	image_data = requests.get(image_url).content
	image_path = f'images{folder}{name}.jpg'
	with open(image_path, 'wb+') as saved_image:
		saved_image.write(image_data)
	if thumbnail:
		new_image = Image.open(image_path)
		new_image.thumbnail((500, 500), Image.ANTIALIAS)
		new_image.save(image_path)	
	return f'/{image_path}'