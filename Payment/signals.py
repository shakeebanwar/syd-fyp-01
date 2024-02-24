from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account
from account.models import User  # Import your custom user model here
from django.conf import settings
from notifications.util import send_credit_notification

User = settings.AUTH_USER_MODEL
@receiver(post_save, sender=User)  # Use your custom user model here
def create_initial_payment(sender, instance, created, **kwargs):
    print("Adding connects to the account")
    if created:
        Account.objects.create(user=instance, connects=250)
        send_credit_notification(instance, 250)
        # send_connects_added_notification(instance, 250)

        
