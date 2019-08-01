from django.contrib import admin

from .models import Request, ParseResult


class RequestAdmin(admin.ModelAdmin):
	fields = ['url', 'handling_time']
	list_display = ('url', 'handling_time', 'is_success')

admin.site.register(Request, RequestAdmin)
admin.site.register(ParseResult)