import sched
import time
import datetime
import threading
import socket
import ast
import json

import django
from django.core.management.base import BaseCommand
from Parser.models import Request, ParseResult


# возвращает null если не достучался

# client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_sock.connect(('127.0.0.1', 81))
# client_sock.sendall(b'https://gist.github.com/mdonkers/63e115cc0c79b4f6b8b3a6b797e485c7')
# data = client_sock.recv(1024)
# client_sock.close()
# print('Recieved', data)

def time_func():
	return datetime.datetime.now(datetime.timezone.utc)
	# return django.utils.timezone.now()

def delay_func(delay):
	seconds = 0
	if delay is datetime.timedelta:
		seconds = delay.total_seconds()
	# seconds = timedelta.total_seconds()
	time.sleep(seconds)
# TIME_FUNC = datetime.datetime.now
TIME_FUNC = time_func
DELAY_FUNC = delay_func
SCHEDULER = sched.scheduler(TIME_FUNC, DELAY_FUNC)

def handler(request):
	# print(TIME_FUNC().strftime('%d.%m.%Y %H:%M:%S'))
	# print('Format in script: ', TIME_FUNC(), type(TIME_FUNC()))

	client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_sock.connect(('127.0.0.1', 81))
	client_sock.sendall(bytes(request, 'cp1251'))
	data = client_sock.recv(1024)
	client_sock.close()
	print('Recieved', data)
	if data == b'null':
		return
	str_data = data.decode('utf-8')
	dict_from_data = ast.literal_eval(str_data)
	print(str_data)
	# data = ast.literal_eval(str_data)
	print(f'Data type {type(dict_from_data)}')
	request_obj = Request.objects.filter(url=request).first()
	if ParseResult.objects.filter(request=request_obj).exists():
			return
		# page_content = parse(request_obj.url)
	if dict_from_data is not None:
		ParseResult.objects.create(
			request=request_obj,
			encoding=dict_from_data['encode'],
			title=dict_from_data['title'],
			h1=dict_from_data['h1'])


def add_sheduled_request(request, datetime):
	SCHEDULER.enterabs(datetime, 0, handler, kwargs={'request': request})
	# print(request, type(request))

def load_request():
	# requests = Request.objects.filter(handling_time__gte = TIME_FUNC())
	requests = Request.objects.filter(handling_time__lte=TIME_FUNC())
	for r in requests:
		add_sheduled_request(r.url, r.handling_time)
		# print('Format in DB: ', r.handling_time, type(r.handling_time))
	SCHEDULER.run(blocking=True)

class Command(BaseCommand):
	help = 'Shedule requests from DB'

	def handle(self, *args, **kwargs):
		load_request()