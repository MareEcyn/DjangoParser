from django.shortcuts import render

from .models import Request, ParseResult

def index(request):
	requests = Request.objects.all()
	results = ParseResult.objects.all()
	context = {
		'requests': requests,
		'results': results,
	}
	return render(request, 'parser/index.html', context)