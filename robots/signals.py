from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order
from robots.models import Robot
from robots.utils import send_email


@receiver(post_save, sender=Robot)
def send_email_to_customer(sender, instance, created, *args, **kwargs):
    if created:
        print('sent email')

        b=Order.objects.filter(robot_serial=instance.serial).select_related('customer')
        if b:
            for i in b:
                send_email(email=i.customer.email,
                       subject_='Robot Signal Notification',
                       context_={'model':instance.model, 'version':instance.version })