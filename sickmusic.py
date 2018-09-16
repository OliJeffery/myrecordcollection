import pathlib
from flask import Flask
from flask import request as params
from flask import send_from_directory
from sick_classes.search import Search
from sick_classes.page import Page

APP = Flask(__name__)

# ROUTING

@APP.route('/search/')
def page_search_results():
	search_string = params.args['s']
	search_results = Search()
	html = search_results.return_results(search_string=search_string)
	return html

@APP.route('/static/<path:folder>/<path:filename>')
def static_files(filename, folder):
	return send_from_directory(f'static/{folder}', filename)

@APP.route('/masters/<path:title>/<path:resource_id>')
def masters_page(title,resource_id):
	resource_url = f"/masters/{resource_id}?title={title}"
	page = Page(resource_url=resource_url)
	return page.release_page()

	