""" Gets a user token which we can use to make further requests """

import json
from os import path
import requests
from decorators.decorators import html_page
from flask import url_for
from PIL import Image
import random
import re


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
			'key':self.api_key,
			'secret':self.api_secret,
			'q':search_str,
			'type':'artist,master',
			#'sort':'year',
			'sort_order':'desc',
			#'per_page':'15'
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
					return f"WTF is {search_str}."
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
		if item['cover_image'] != 'https://img.discogs.com/images/spacer.gif':
			self.cover_image = item['cover_image']
			self.thumbnail = item['thumb']
		else:
			self.cover_image = ''
			self.thumbnail = ''
		self.type = item['type']

	def preview(self):
		red = random.randint(150, 255)
		green = random.randint(30, 50)
		blue = random.randint(30, 50)
		tranlucence = (random.randint(35,55))/100
		self.pretty_url = f'/{self.type}s/'+re.sub('[^a-zA-Z\d-]', '', self.title).lower()
		self.full_url = f"{self.pretty_url}/{self.id}"
		preview = f"""
			<div class="preview" id="preview_{self.id}" data-resource-url='{self.resource_url}' data-full-url='{self.full_url}' data-title='{self.title}' data-pretty-url='{self.pretty_url}'>
				<h2>{self.title}</h2>
				<div class="image" data-lazy-load='{self.cover_image}' style='background-image: url("{self.thumbnail}")'></div>
				<div class="overlay" style="background:rgba({red},{green},{blue},{tranlucence})"></div>
			</div>
		"""
		return preview
