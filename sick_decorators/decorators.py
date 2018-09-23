from functools import wraps
from flask import request
from sick_classes.spotify_connection import SpotifyConnection
from sick_classes.mysql_connector import Database

def html_page(body_html):
	@wraps(body_html)
	def wrapper(*args, **kwargs):
		access_token = request.cookies.get('access_token')
		try:
			login = profile_info(access_token)
		except KeyError:
			login = login_link()
		header = open('html/header.html').read().format(login)
		footer = open('html/footer.html').read()
		html = body_html(*args, **kwargs)
		return f"{header}{html}{footer}"
	return wrapper

def profile_info(access_token):
	connection = SpotifyConnection()
	connection.token = access_token
	user_info = connection.make_request('me')
	display_name = user_info['display_name']
	profile_pic = user_info['images'][0]['url']
	html = f"<div class='profile_pic' style='background-image:url({profile_pic})' data-display-name='{display_name}'>"
	html = user_info
	return html

def login_link():
	return "<a class='login' href='/login'>Login via Spotify</a>"