from datetime import datetime, timezone

from django.shortcuts import render

from .models import Request, ParseResult
from .server import parse

def index(request):
	requests = Request.objects.filter(handling_time__lte = datetime.now(timezone.utc)).order_by('-handling_time')
	for request_obj in requests:
		if ParseResult.objects.filter(request=request_obj).exists():
			continue
		page_content = parse(request_obj.url)
		if page_content is not None:
			ParseResult.objects.create(
				request=request_obj,
				encoding=page_content['encode'],
				title=page_content['title'],
				h1=page_content['h1'])
	results = ParseResult.objects.all()
	context = {
		'requests': requests,
		'results': results,
	}
	return render(request, 'parser/index.html', context)