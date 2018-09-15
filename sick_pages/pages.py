from classes.classes import DiscogsConnection, Artist
from decorators.decorators import html_page

@html_page
def page(*args):
	return html

@html_page
def search_results(search_string):
	connection = DiscogsConnection()
	html = connection.search(search_string)
	return html

@html_page
def master_page(resource_url):
	return resource_url
