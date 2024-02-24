from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from django.core.validators import MinValueValidator, MaxValueValidator


class Client(models.Model):
    # One-to-one relationship with the User model
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.user.name
    
from Seller.models import Seller
class Recent_Freelancer(models.Model):
    recent_freelancer = models.ForeignKey(Seller, on_delete=models.CASCADE)
    clients = models.IntegerField()
    # Add other fields relevant to the Recent_Freelancer model

    def __str__(self):
        return self.recent_freelancer.name
def name_file(instance, filename):
    return '/'.join(['images', str(instance.client.user_id)])

class ProfilePicture(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE,related_name='profile_picture')
    profile_picture = models.ImageField(upload_to='ProfilePic', blank=True, null=True)

    def __str__(self):
        return f"Profile Picture for {self.client.user_id}"
