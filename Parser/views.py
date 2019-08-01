from datetime import datetime, timezone

from django.shortcuts import render

from .models import Request, ParseResult
from .parser import parse

def index(request):
	requests = Request.objects.filter(handling_time__lte = datetime.now(timezone.utc)).order_by('-handling_time')
	for request in request:
		console.log(parse(request.url))
	results = ParseResult.objects.all()
	context = {
		'requests': requests,
		'results': results,
	}
	return render(request, 'parser/index.html', context)