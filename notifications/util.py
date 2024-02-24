from django.contrib.auth import get_user_model
from .models import Notification
from django.utils import timezone
def send_credit_notification(user, credits_added):
    content = f"🎉 Welcome to BNR360 Platform! 🚀"
    timestamp = timezone.now()

    Notification.objects.create(
        recipient=user,
        content=content,
        timestamp=timestamp
    )

def send_hire_notification(user,job):
    content = f"You have been hired for job {job.job_title}."
    timestamp = timezone.now()

    Notification.objects.create(
        recipient=user,
        content=content,
        timestamp=timestamp,
        extras={"job_id":job.id}
    )

def send_message_notification(user,sender,roomid):
    content = f"You have new notification from user {sender}."
    timestamp = timezone.now()

    Notification.objects.create(
        recipient=user,
        content=content,
        timestamp=timestamp,
        extras={"room_id":roomid}

    )
def send_course_notification(user, credits_added,course):
    content = f"Congrats you finished this {course} course.{credits_added} credits have been added to your account."
    timestamp = timezone.now()

    Notification.objects.create(
        recipient=user,
        content=content,
        timestamp=timestamp
    )

def send_seller_success_notification(user,title):
    content = f"Congrats, payment successfully transfered to your account of job {title}."
    timestamp = timezone.now()

    Notification.objects.create(
        recipient=user,
        content=content,
        timestamp=timestamp
    )
def send_seller_fail_notification(user,title):
    content = f"Payment is failed by Client on job {title}."
    timestamp = timezone.now()

    Notification.objects.create(
        recipient=user,
        content=content,
        timestamp=timestamp
    )
def send_client_success_notification(user,title):
    content = f"Congrats, payment has been tranfer to Freelancer on job {title}."
    timestamp = timezone.now()

    Notification.objects.create(
        recipient=user,
        content=content,
        timestamp=timestamp
    )
def send_client_fail_notification(user,title):
    content = f"Payment tranfer failed on job {title}."
    timestamp = timezone.now()

    Notification.objects.create(
        recipient=user,
        content=content,
        timestamp=timestamp
    )

def send_seller_job_completed(user,title):
    content = f"Your job '{title}' has been accepted by client and is now completed."
    timestamp = timezone.now()

    Notification.objects.create(
        recipient=user,
        content=content,
        timestamp=timestamp
    )