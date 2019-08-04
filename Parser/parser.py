import re
import urllib.request as request


def parse(url):
	"""
	Parse given URL and return dictionary of strings (empty string if particular element does not exist).
	Return None for any urllib error.
	"""
	url = url.decode("utf-8")
	html = ''
	try:
		with request.urlopen(url) as response:
			html = str(response.read())
	except:
		return None
	encode = re.search("charset=\"([^>]+)\"", html)
	title = re.search("<title>(.*)</title>", html)
	h1 = re.search("<h1.*>(.*)</h1>", html)
	output = {}
	output['h1'] = h1.group(1) if h1 is not None else ''
	output['title'] = title.group(1) if title is not None else ''
	output['encode'] = encode.group(1) if encode is not None else ''
	return output