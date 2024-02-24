from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Seller(models.Model):
    # One-to-one relationship with the User model
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()
    personal_website=models.TextField(max_length=200)
    # phone_number = models.CharField(max_length=12)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)

    def __str__(self):
        return self.user.name
    def calculate_overall_rating(self):
        ratings = Rating.objects.filter(seller=self)
        if ratings:
            total_ratings = sum(rating.value for rating in ratings)
            overall_rating = total_ratings / len(ratings)
            return round(overall_rating, 2)
        return 0.0
class Image(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='seller_pictures/')

    def __str__(self):
        return f"Image for {self.seller.user.name}"
class Rating(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),  # Minimum value is 1
            MaxValueValidator(5)   # Maximum value is 5
        ]
    )
    review = models.TextField(blank=True)  # Optional review
    
    def __str__(self):
        return f"Rating by {self.user} for {self.seller}"
    class Meta:
        # Make the combination of user and seller unique
        unique_together = ('user', 'seller')
class ProfilePicture(models.Model):
    seller = models.OneToOneField(Seller, on_delete=models.CASCADE,related_name='profile_picture')
    profile_picture = models.ImageField(upload_to='ProfilePic_seller', blank=True, null=True)

class Portfolio(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='portfolios')
    profile_picture = models.ImageField(upload_to='Portfolio', blank=True, null=True) 
    url = models.URLField(max_length=200) 


class Education(models.Model):
    seller = models.OneToOneField(Seller, on_delete=models.CASCADE, related_name='education')
    education = models.CharField(max_length=100)
    from_year = models.DateField()
    to_year = models.DateField()

class Language(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE,related_name='languages')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Skill(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE,related_name='skills')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name