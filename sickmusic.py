import pathlib
from flask import Flask
from flask import request as params
from flask import send_from_directory
from sick_classes.spotify_connection import SpotifyConnection
from sick_decorators import html_page

APP = Flask(__name__)

# ROUTING

SPOTIFY = SpotifyConnection()

@APP.route('/')
@html_page
def home():
	try:
		search_string = params.args['s']
		return str(SPOTIFY.search(search_string))
	except KeyError:
		return('Home sweet home')


@APP.route('/static/<path:folder>/<path:filename>')
def static_files(filename, folder):
	return send_from_directory(f'static/{folder}', filename)

@APP.route('/<path:artist>/<path:release>/<path:resource_id>')
@html_page
def render_resource(artist, release, resource_id):
	if release is not None:
		return SPOTIFY.release(resource_id)

