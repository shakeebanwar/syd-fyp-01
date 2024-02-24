from django.db import models
from django.conf import settings
from djangoauth.storage_backends import AzureMediaStorage

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()  # Add a TextField for the description
    total_duration = models.PositiveIntegerField()  # Add a field for total duration in minutes
    thumbnail = models.ImageField(upload_to='course_thumbnails/', null=True, blank=True)

class Video(models.Model):
    title = models.CharField(max_length=100)
    # file = models.FileField(upload_to='videos/', storage=AzureMediaStorage())
    file = models.FileField(upload_to='videos/')
    course = models.ForeignKey(Course, related_name='videos', on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='progress', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)
