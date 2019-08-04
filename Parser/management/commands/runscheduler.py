import sched
import time
import datetime
import threading

import django
from django.core.management.base import BaseCommand
from Parser.models import Request

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

def handler():
	# print(TIME_FUNC().strftime('%d.%m.%Y %H:%M:%S'))
	print('Format in script: ', TIME_FUNC(), type(TIME_FUNC()))

def add_sheduled_request(request, datetime):
	SCHEDULER.enterabs(datetime, 0, handler, ())

def load_request():
	# requests = Request.objects.filter(handling_time__gte = TIME_FUNC())
	requests = Request.objects.filter(handling_time__gte=TIME_FUNC())
	for r in requests:
		add_sheduled_request('', r.handling_time)
		print('Format in DB: ', r.handling_time, type(r.handling_time))
	SCHEDULER.run(blocking=True)

class Command(BaseCommand):
	help = 'Shedule requests from DB'

	def handle(self, *args, **kwargs):
		load_request()