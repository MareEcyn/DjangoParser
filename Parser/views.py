from datetime import datetime, timezone

from django.shortcuts import render
from .models import Request, ParseResult


def index(request):
	requests = Request.objects.filter(handling_time__lte = datetime.now(timezone.utc)).order_by('-handling_time')
	results = ParseResult.objects.all()
	context = {
		'requests': requests,
		'results': results,
	}
	return render(request, 'parser/index.html', context)