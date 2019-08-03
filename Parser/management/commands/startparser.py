from django.core.management.base import BaseCommand, CommandError
import subprocess

class Command(BaseCommand):
	help = "Run Django WSGI server and Parser server"
	def handle(self, *args, **options):
		self.stdout.write("crya")