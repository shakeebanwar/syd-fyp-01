from django.db import models
from django.conf import settings
from jobpost.models import JobPost
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver, Signal
from Seller.models import Seller
from Client.models import Client
from django.utils import timezone
import stripe
import uuid
from django.conf import settings


class StripeAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    account_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    connects = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.user.username}'s Account"
# @receiver(post_save, sender=Account)
# def update_verified_field(sender, instance, **kwargs):
#     # This signal handler updates the verified field when the associated account's balance changes
#     try:
#         user = instance.user
#     except settings.AUTH_USER_MODEL.DoesNotExist:
#         return

#     if instance.balance > 0:
#         JobPost.objects.filter(client=user.client).update(verified=True)
#     else:
#         JobPost.objects.filter(client=user.client).update(verified=False)
class Payment(models.Model):
    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Add a UUID field as the primary key
    job = models.OneToOneField(JobPost, on_delete=models.CASCADE, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Amount in dollars
    created_at = models.DateTimeField(auto_now_add=True)
    payment_date = models.DateTimeField(default=timezone.now)
    price_id = models.CharField(max_length=255, blank=True, null=True)
    intent_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ), default='pending')

# @receiver(pre_save, sender=Payment)
# def pre_save_payment(sender, instance, **kwargs):
#     print("hello")
#     try:
#         project_budget = instance.job.project_budget
#         client_id = instance.job.client
#         freelance_id = instance.job.freelancer
#         instance.amount = project_budget
#         instance.client = client_id
#         instance.freelancer = freelance_id
#     except Exception as e:
#         # Handle any exceptions that may occur if relationships are missing or data is not available
#         # print(e)
#         pass

# @receiver(post_save, sender=Payment)
# def create_stripe_price(sender, instance, created, **kwargs):
#         try:
#             # pre_save.disconnect(pre_save_payment, sender=Payment)
#             # Get the price amount from the instance or request data (adapt as needed)
#             price_amount = instance.amount  # Assuming the amount is in cents

#             if price_amount is None:
#                 pass
#                 # Handle the case where the price amount is missing
#             # product = stripe.Product.create(
#             #     name='hello world',
#             #     type='service',  # Replace with 'service' or 'good' as appropriate
#             #     # Add other product details as needed
#             # )
#             price_amount_cents = int(price_amount * 100)
#             price = stripe.Price.create(
#                 unit_amount=price_amount_cents,
#                 currency='usd',  # Replace with the appropriate currency code
#                 recurring=None,  # No recurrence for one-time payments
#                 product_data={
#                     'name': 'software',
#                     # Add other product data as needed
#                 }
#             )

#             # Set the price_id in the payment model
#             instance.price_id = price.id
#             instance.save()
#             # pre_save.connect(pre_save_payment, sender=Payment)
#         except Exception as e:
#             print(e)
#             # Handle any exceptions that may occur during the Stripe Price creation
#             pass

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from account.models import User 
# @receiver(post_save, sender=User)  # Use your custom user model here
# def create_initial_payment(sender, instance, created, **kwargs):
#     print("Adding connects to the account")
#     if created:
#         Payment.objects.create(user=instance, amount=250)

