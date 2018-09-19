from functools import wraps

def html_page(body_html):
	@wraps(body_html)
	def wrapper(*args, **kwargs):
		header = open('html/header.html').read()
		footer = open('html/footer.html').read()
		html = body_html(*args, **kwargs)
		return header+html+footer
	return wrapper
