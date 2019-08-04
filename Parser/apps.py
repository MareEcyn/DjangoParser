from django.apps import AppConfig


class ParserConfig(AppConfig):
    name = 'Parser'

    def ready(self):
    	import Parser.signals
