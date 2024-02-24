from django.db import models
from django.conf import settings
from django.db.models import JSONField
  # Or your custom User model if applicable

class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    extras = JSONField(blank=True, null=True)
    def mark_as_read(self):
        self.is_read = True
        self.save()
    class Meta:
        ordering = ['-timestamp']  # Order notifications by timestamp, most recent first

    def __str__(self):
        return self.content
