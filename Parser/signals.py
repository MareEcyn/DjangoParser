import uuid
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Request

callback_uid = uuid.uuid4()

@receiver(post_save, sender=Request, dispatch_uid=callback_uid)
def handle_add_request(sender, **kwargs):
	print(f'{sender.objects.last().handling_time}')

@receiver(pre_delete, sender=Request, dispatch_uid=callback_uid)
def handle_del_request(sender, **kwargs):
	print(f'sender url: {sender.url}')