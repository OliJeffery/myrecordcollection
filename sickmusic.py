import pathlib
from flask import Flask
from flask import request as params
from flask import send_from_directory
from sick_pages import pages
from PIL import Image

BASE_URL = 'https://api.discogs.com'

app = Flask(__name__)

# CSS

@app.route('/css/sickmusic.css')
def css():
	with open('css/sickmusic.css') as css:
		return css.read()

# IMAGES
@app.route('/images/<path:folder>/<path:filename>')
def image_path(filename, folder):
	return send_from_directory(f'images/{folder}', filename)

# ROUTING

@app.route('/')
def page_home():
	return pages.page('whut')

@app.route('/search/')
def page_search_results():
	search_string = params.args['s']
	return pages.search_results(search_string)

@app.route('/artist/')
def page_artist(artist_id):
	pass

@app.route('/static/<path:folder>/<path:filename>')
def static_files(filename, folder):
	return send_from_directory(f'static/{folder}', filename)

@app.route('/<path:item_type>/<path:title>/<path:resource_id>')
def basic_page(item_type,title,resource_id):
	resource_url = f"{BASE_URL}/{item_type}/{resource_id}"
	return pages.master_page(resource_url)