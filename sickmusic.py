import pathlib
from flask import Flask
from flask import request as params
from flask import send_from_directory
from sick_classes.spotify_connection import SpotifyConnection
from sick_decorators import html_page

APP = Flask(__name__)

# ROUTING

@APP.route('/static/<path:folder>/<path:filename>')
def static_files(filename, folder):
	return send_from_directory(f'static/{folder}', filename)

@APP.route('/')
@html_page
<<<<<<< HEAD
def home():
	try:
		search_string = params.args['s']
		spotify = SpotifyConnection()
		return str(spotify.search(search_string))
	except KeyError:
		return('Home sweet home')
	
=======
def search():
	search_string = params.args['s']
	spotify = SpotifyConnection()
	return str(spotify.search(search_string))
>>>>>>> be5dc705b22ddc4d93e029dfd3b173e977001273
