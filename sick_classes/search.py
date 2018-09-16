from sick_classes.discogs import DiscogsConnection
import re
import random
from sick_decorators import html_page

class Search(DiscogsConnection):
	
	@html_page
	def return_results(self, search_string):
		params = {
			'q':search_string,
			'type':'artist,master',
			'sort_order':'desc',
			#'per_page':'15'
		}
		url = f"database/search"
		search_results = self.get_resource(url, params)
		pagination = search_results['pagination']
		results = search_results['results']
		if(len(results)>0):
			html = ''
			for result in results:
				html+=self.preview(result)
			return html
		else:
			return "Huh?"			

	def preview(self, item):
		red = random.randint(150, 255)
		green = random.randint(30, 50)
		blue = random.randint(30, 50)
		tranlucence = (random.randint(35,55))/100
		pretty_url = f"/{item['type']}s/"+re.sub('[^a-zA-Z\d-]', '', item['title']).lower()
		full_url = f"{pretty_url}/{item['id']}"
		preview = f"""
			<div class="preview" id="preview_{item['id']}" data-resource-url='{item['resource_url']}' data-full-url='{full_url}' data-title='{item['title']}' data-pretty-url='{pretty_url}'>
				<h2>{item['title']}</h2>
				<div class="image" data-lazy-load='{item['cover_image']}' style='background-image: url("")'></div>
				<div class="overlay" style="background:rgba({red},{green},{blue},{tranlucence})"></div>
			</div>
		"""
		return preview


