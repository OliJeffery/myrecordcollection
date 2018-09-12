import pathlib
from flask import Flask
from flask import request as params
from flask import send_from_directory
from sick_pages import pages
from PIL import Image

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

