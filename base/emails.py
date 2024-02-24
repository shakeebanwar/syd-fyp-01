from django.conf import settings
from django.core.mail import send_mail


def send_account_activation_email(email,email_token):
    subject = 'Congratulations!'
    email_from = settings.EMAIL_HOST_USER
    message = f'Congratulations! Your registration is now complete. Thank you for choosing our services. We look forward to serving you with excellence.'
    
    send_mail(subject, message, email_from, [email])

def send_account_reset_email(email,email_token,uid):
    subject = 'To reset your password'
    email_from = settings.EMAIL_HOST_USER
    message = f'Hello, Click on the link to Reset your account http://localhost:3000/verify/{uid}/{email_token}'
    
    send_mail(subject, message, email_from, [email])