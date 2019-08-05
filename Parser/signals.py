import uuid

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Request


UID = uuid.uuid4()

@receiver(post_save, sender=Request, dispatch_uid=UID)
def handle_add_request(sender, **kwargs):
	pass

@receiver(pre_delete, sender=Request, dispatch_uid=UID)
def handle_del_request(sender, **kwargs):
	pass