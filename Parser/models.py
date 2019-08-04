import django.dispatch
import time
from datetime import datetime, timezone
from django.db import models


class Request(models.Model):
	url = models.URLField('parsing URL')
	# handling_time = models.DateTimeField('handling time', default=datetime.now(timezone.utc))
	handling_time = models.DateTimeField('handling time', default=django.utils.timezone.now)

	def __str__(self):
		return self.url

	def is_success(self):
		# now = datetime.now(timezone.utc)
		now = django.utils.timezone.now()
		if self.handling_time > now:
			return None
		return ParseResult.objects.filter(request=self).exists()

	is_success.short_description = 'success'
	is_success.boolean = True

class ParseResult(models.Model):
	request = models.OneToOneField(Request, primary_key=True, on_delete=models.CASCADE)
	encoding = models.CharField('page encoding', max_length=10, blank=True)
	title = models.TextField('page title', blank=True)
	h1 = models.TextField('<h1> tag', blank=True)

	def __str__(self):
		return "Resource: %s" % self.request.url

	def is_empty(self):
		if self.encoding == '' and self.title == '' and self.h1 == '':
			return True
		return False