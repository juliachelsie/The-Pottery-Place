from django.db.models.signals import post_save, post_delete
from django.dispatch import reciever

from .models import OrderItem

@reciever(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    instance.order.update_total_cost()


@reciever(post_delete, sender=OrderLineItem)
def update_on_save(sender, instance, **kwargs):
    instance.order.update_total_cost()
    