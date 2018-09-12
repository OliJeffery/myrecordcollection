from classes.classes import DiscogsConnection, Artist
from decorators.decorators import html_page

@html_page
def page(html):
	return html

@html_page
def search_results(search_string):
	connection = DiscogsConnection()
	html = connection.search(search_string)
	return html