# in dispute/models.py
from django.db import models
from django.conf import settings
from jobpost.models import JobPost


class Dispute(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    jobpost = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='jobpost')
    title = models.CharField(max_length=255)
    text = models.TextField()
    resolved = models.BooleanField(default=False) 
    def __str__(self):
        return self.title


from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=15)
    email = models.EmailField()
    text = models.TextField()

    def __str__(self):
        return self.name
