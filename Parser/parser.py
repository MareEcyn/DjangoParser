import urllib.request as request
import re


def parse(url):
	"""
	Parse given URL and return dictionary of strings (empty string if particular element does not exist).
	Return None for any urllib error.
	"""
	html = ''
	try:
		with request.urlopen(url) as response: # valid check, exceptions catch
			html = response.read()
	except:
		return None
	encode = re.search("<meta charset=\"([^>]+)\"", str(html))
	title = re.search("<title>(.*)</title>", str(html))
	h1 = re.search("<h1>(.*)</h1>", str(html))
	output = {}

	# if encode is not None:
	# 	output['encode'] = encode.group(1)
	# else:
	# 	output['encode'] = ''
	# if title is not None:
	# 	output['title'] = title.group(1)
	# else:
	# 	output['title'] = ''
	# if h1 is not None:
	# 	output['h1'] = h1.group(1)
	# else:
	# 	output['h1'] = ''

	output['h1'] = h1.group(1) if h1 is not None else ''
	output['title'] = title.group(1) if title is not None else ''
	output['encode'] = encode.group(1) if encode is not None else ''
	return output

# o = parse('https://docs.python.org/3/library/re.html?highlight=re#match-objects')
# print(o)