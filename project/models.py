from django.db import models
from Seller.models import Seller

class work(models.Model):
    Seller = models.OneToOneField(Seller, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='pictures_project/', blank=True, null=True)
    text = models.TextField()
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user
    




    
class Project(models.Model):
    Seller = models.OneToOneField(Seller, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Skill(models.Model):
    Project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Tag(models.Model):
    Project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
