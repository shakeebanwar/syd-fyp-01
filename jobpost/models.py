from django.db import models
from Client.models import Client
from Seller.models import Seller
from django.conf import settings

class JobPost(models.Model):
    TERM_CHOICES = (
        ('short', 'Short Term'),
        ('long', 'Long Term'),
    )
    SCOPE_CHOICES = (
        ('large', 'Large'),
        ('medium', 'Medium'),
        ('small', 'Small'),
    )
    LENGTH_CHOICES = (
        ('3-6', '3 to 6 months'),
        ('1-3', '1 to 3 months'),
        ('1', 'Less than 1 month'),
    )
    EXPERIENCE_CHOICES = (
        ('entry', 'Entry'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    )
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('completed', 'Completed')
    ), default='pending')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    term = models.CharField(max_length=10, choices=TERM_CHOICES)
    job_title = models.TextField()
    skills = models.ManyToManyField('Skill')
    scope = models.CharField(max_length=10, choices=SCOPE_CHOICES)
    length = models.CharField(max_length=5, choices=LENGTH_CHOICES)
    experience_needed = models.CharField(max_length=15, choices=EXPERIENCE_CHOICES)
    hire_opp = models.BooleanField()
    project_budget = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    freelancer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    numofproposals = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)  # New field for verification

    # def save(self, *args, **kwargs):
    #     # Check if the associated account's balance is greater than 0
    #     if self.client.user.account.balance > 0:
    #         self.verified = True
    #     else:
    #         self.verified = False

    #     super().save(*args, **kwargs)
    def __str__(self):
        return self.job_title

class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class SavedJob(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.seller} saved {self.job_post}"