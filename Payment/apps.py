from django.apps import AppConfig


class PaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Payment'

# Payment/apps.py

from django.apps import AppConfig

class PaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Payment'  # Use the correct app name here

    def ready(self):
        import Payment.signals  # Import your signals.py file here
