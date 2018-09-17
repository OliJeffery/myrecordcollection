"""Release class"""

from sick_classes.discogs import DiscogsConnection
from sick_decorators import html_page, list_widget

class Page(DiscogsConnection):

	def __init__(self, resource_url):
		DiscogsConnection.__init__(self)
		self.resource_url = resource_url

	@html_page
	def release_page(self):
		release_resource = self.get_resource(self.resource_url, authenticate=True)
		#main_release_url = master_resource['main_release_url']
		#release_resource = self.get_resource(main_release_url, full_url=True)
		#release_resource['videos']
		#release_resource['labels']
		#release_resource['year']
		#release_resource['images']
		#
		#release_resource['genre']
		#release_resource['artists']
		
		release_cover = release_resource['images'][0]['uri']
		tracklist = self.get_tracklist(release_resource['tracklist'])
		artists = release_resource['artists']
		artists_list = self.get_artists_list(artists)
		html = f"""
			<img src='{release_cover}' class='release_cover' />
			<h2>{release_resource['title']} ({release_resource['released']}) by {artists_list}</h2>
			{tracklist}
			
		"""


		return(html)

	def get_tracklist(self, tracklist):
		list_version = []
		for track in tracklist:
			list_version.append(f"{track['title']}")
		html = '<ol><li>'+'</li><li>'.join(list_version)+'</li></ol>'
		return html

	def get_artists_list(self, artists):
		list_version = []
		for artist in artists:
			list_version.append(f"{artist['name']}")
		html = ', '.join(list_version)
		return html