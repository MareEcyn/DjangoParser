from django.db import models


class Request(models.Model):
	url = models.URLField('parsing URL')
	handling_time = models.DateTimeField('handling time')

	def __str__(self):
		return self.url

	def is_success(self):
		result = ParseResult.objects.get(pk=1)
		return str(result)

	is_success.short_description = 'success'

class ParseResult(models.Model):
	request = models.OneToOneField(Request, primary_key=True, on_delete=models.CASCADE)
	encoding = models.CharField('page encoding', max_length=10)
	title = models.TextField('page title', blank=True)
	h1 = models.TextField('<h1> tag', blank=True)

	def __str__(self):
		return "Parse result for: %s" % self.request.url