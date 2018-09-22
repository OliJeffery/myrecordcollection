from functools import wraps
from flask import request
from sick_classes.spotify_connection import SpotifyConnection

def html_page(body_html):
	@wraps(body_html)
	def wrapper(*args, **kwargs):
		access_token = request.cookies.get('access_token')
		if access_token is None:
			login = "<a class='login' href='/login'>Login via Spotify</a>"
		else:
			login = profile_info(access_token)
		header = open('html/header.html').read().format(login)
		footer = open('html/footer.html').read()
		html = body_html(*args, **kwargs)
		return header+html+footer
	return wrapper

def profile_info(access_token):
	connection = SpotifyConnection()
	connection.token = access_token
	user_info = connection.make_request('me')
	display_name = user_info['display_name']
	profile_pic = user_info['images'][0]['url']
	html = f"<div class='profile_pic' style='background-image:url({profile_pic})' data-display-name='{display_name}'>"
	return html
	