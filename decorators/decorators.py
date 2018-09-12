def html_page(body_html):
	def wrapper(results):
		header = open('html/header.html').read()
		footer = open('html/footer.html').read()
		html = body_html(results)
		return header+html+footer
	return wrapper
