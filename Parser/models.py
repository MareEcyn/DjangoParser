from datetime import datetime, timezone

from django.db import models


class Request(models.Model):
	url = models.URLField('parsing URL')
	handling_time = models.DateTimeField('handling time')

	def __str__(self):
		return self.url

	def is_success(self): # to-do
		now = datetime.now(timezone.utc)
		if now < self.handling_time:
			return None
		return ParseResult.objects.filter(pk=1).exists()

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