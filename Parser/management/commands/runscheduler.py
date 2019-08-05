import sched
import time
import datetime
import socket
import ast
import sys

from django.core.management.base import BaseCommand
from Parser.models import Request, ParseResult


def time_func():
	return datetime.datetime.now(datetime.timezone.utc)

def delay_func(delay):
	seconds = 0
	if delay is datetime.timedelta:
		seconds = delay.total_seconds()
	time.sleep(seconds)

TIME_FUNC = time_func
DELAY_FUNC = delay_func
SCHEDULER = sched.scheduler(TIME_FUNC, DELAY_FUNC)
SOCK = None
SERV_ADDR = ('127.0.0.1', 81)

def update_model(model_obj, data):
	ParseResult.objects.create(
			request=model_obj,
			encoding=data['encode'],
			title=data['title'],
			h1=data['h1'])

def get_response(request):
	"""
	Manage one cycle of data swop in client-server system.
	Return: bytes object
	"""
	global SOCK
	SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		SOCK.connect(SERV_ADDR)
	except ConnectionRefusedError:
		SOCK.close()
		print('ERROR: Server is not reachable. Check connection settings.')
		sys.exit()
	SOCK.sendall(bytes(request, 'cp1251'))
	response = SOCK.recv(1024)
	SOCK.close()
	return response

def handle(request):
	"""
	Execute model update logic.
	"""
	response = get_response(request)
	if response == b'null' or response == b'':
		return
	response = response.decode('utf-8')
	response_dict = ast.literal_eval(response)
	request_obj = Request.objects.filter(url=request).first()
	if ParseResult.objects.filter(request=request_obj).exists():
		return
	if response_dict is not None:
		update_model(request_obj, response_dict)


def add_event(request, datetime):
	SCHEDULER.enterabs(datetime, 0, handle, kwargs={'request': request})

def load_events(with_old):
	requests = None
	if with_old == True:
		requests = Request.objects.all()
	elif with_old == False:
		requests = Request.objects.filter(handling_time__gte=TIME_FUNC())
	for r in requests:
		add_event(r.url, r.handling_time)

class Command(BaseCommand):
	help = 'Shedule requests to server and manage model update based on response.'

	def handle(self, *args, **kwargs):
		load_events(with_old=True)
		SCHEDULER.run()