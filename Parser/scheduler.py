import sched
import time
import datetime

from models import Request


TIME_FUNC = datetime.datetime.now
DELAY_FUNC = time.sleep
SHEDULER = sched.scheduler(TIME_FUNC, DELAY_FUNC)

def handler():
	print(TIME_FUNC().strftime('%d.%m.%Y %H:%M:%S'))

def add_sheduled_request(request, datetime):
	SHEDULER.enterabs(TIME_FUNC(), 0, handler, ())
	SHEDULER.run()

def load_request():
	requests = Request.objects.filter(handling_time__gte = datetime.now())
	for r in requests:
		print(r.url)

load_request()