import urllib.request as request
import re


def parse(url):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15'
	}
	html = ''
	with request.urlopen(url) as response:
		html = response.read()
	encode = re.search("<meta charset=\"([^>]+)\"", str(html))
	title = re.search("<title>(.*)</title>", str(html))
	h1 = re.search("<h1>(.*)</h1>", str(html))
	output = ''

	if encode is not None:
		output += encode.group(1)
	else:
		output += None
	if title is not None:
		output += title.group(1)
	else:
		output += None
	if h1 is not None:
		output += h1.group(1)
	else:
		output += None
	return output

o = parse('https://docs.python.org/3/howto/urllib2.html')
print(o)