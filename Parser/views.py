from django.shortcuts import render

def index(request):
	return render(request, 'parser/index.html', {})
