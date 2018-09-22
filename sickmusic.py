import pathlib
from flask import Flask
from flask import request as params
from flask import send_from_directory
from flask import make_response
from sick_classes.spotify_search import SpotifySearch
from sick_classes.spotify_render import SpotifyRender
from sick_classes.spotify_user import SpotifyUser
from sick_decorators import html_page

APP = Flask(__name__)

# ROUTING

@APP.route('/')
@html_page
def home():
	try:
		spotify_search = SpotifySearch()
		search_string = params.args['s']
		return str(spotify_search.search(search_string))
	except KeyError:
		return('Home sweet home')


@APP.route('/static/<path:folder>/<path:filename>')
def static_files(filename, folder):
	return send_from_directory(f'static/{folder}', filename)

@APP.route('/<path:artist>/<path:release>/<path:resource_id>')
@html_page
def render_resource(artist, release, resource_id):
	spotify_release = SpotifyRender()
	if release is not None:
		return spotify_release.release(resource_id)

@APP.route('/login')
def login_to_spotify():
	referrer = params.referrer # Need to make sure this can't be done via an offsite link
	user = SpotifyUser()
	return user.login(referrer)

@APP.route('/login_callback')
def login_callback():
	code = params.args['code']
	user = SpotifyUser()
	token_info = user.get_access_token(code)
	access_token = token_info['access_token']
	expiration = token_info['expires_in']
	refresh_token = token_info['refresh_token']
	referrer = params.cookies['referrer']
	response = make_response(user.redirect_to(referrer))
	response.set_cookie('access_token', access_token)
	response.set_cookie('expiration', str(expiration))
	response.set_cookie('refresh_token', refresh_token)
	return response
