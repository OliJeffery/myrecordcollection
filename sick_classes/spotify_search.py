import random
import re
from .spotify_connection import SpotifyConnection

class SpotifySearch(SpotifyConnection):

	def search(self, query):
		payload = {'q':query, 'type':'artist,album', 'limit':'15', 'market':'GB'}
		results = self.make_request('search', payload)
		html = ''
		html+=self.preview(results['artists']['items'][0])
		for album in results['albums']['items']:
			html+=self.preview(album)
		return html

	def preview(self, item):
		tranlucence = (random.randint(35,55))/100
		item_type = item['type']
		if item_type=='album':
			item_type = item['album_type']
		if item_type == 'artist':
			red = random.randint(30, 50)
			green = random.randint(30, 50)
			blue = random.randint(150, 255)		
		elif item_type == 'album':
			red = random.randint(150, 255)
			green = random.randint(30, 50)
			blue = random.randint(30, 50)		
		elif item_type == 'single':
			red = random.randint(30, 50)
			green = random.randint(150, 255)
			blue = random.randint(30, 50)
		else:
			red = random.randint(30, 50)
			green = random.randint(30, 50)
			blue = random.randint(30, 50)		
		if 'artists' in item.keys():
			artist = item['artists'][0]['name']
		else:
			artist = ''
		pretty_url = (re.sub('[^a-zA-Z\d-]', '-', artist) + '/' + re.sub('[^a-zA-Z\d-]', '-', item['name'])).lower()
		full_url = f"{pretty_url}/{item['id']}"
		try:
			just_the_year = item['release_date'].split('-')[0]
			release_year = " ("+just_the_year+")"
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