from .spotify_connection import SpotifyConnection

class SpotifyRender(SpotifyConnection):

	def release(self, resource_id):
		endpoint = f'albums/{resource_id}'
		#return str(self.make_request(endpoint))
		release = self.make_request(endpoint)
		release_cover = release['images'][0]['url']
		html = f"<img class='release_cover' src='{release_cover}'>"
		return html