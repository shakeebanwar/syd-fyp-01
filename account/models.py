from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
import uuid
from django.db.models.signals import post_save
from rest_framework_simplejwt.tokens import RefreshToken
from django.dispatch import receiver
from base.emails import send_account_activation_email


# Create your models here.
ROLE_CHOICES = (
    ('none', 'None'),
    ('seller', 'Seller'),
    ('client', 'Client'),
)
class UserManager(BaseUserManager):
    def create_user(self,email,name,password=None,password2=None):

        if not email:
            raise ValueError('User not have an email')
        
        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,name,password=None):
        
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin=True
        user.save(using=self._db)
        return user
AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}
from shortuuidfield import ShortUUIDField

class User(AbstractBaseUser):
    userId = ShortUUIDField()
    email= models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    tc = models.BooleanField(default=True)
    is_email_verified=models.BooleanField(default=False)
    email_token = models.CharField(max_length=100,null=True,blank=True)
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='none')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['name']

    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
    
    @property
    def is_staff(self):
        return self.is_admin
    
class OnlineUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username

@receiver(post_save, sender=User)
def send_email_token(sender, instance, created, **kwrags):
    print("Sending email to the user")
    try:
        if created:
            email_token = str(uuid.uuid4())
            instance.email_token = email_token
            instance.save()
            email=instance.email
            # email_token = str(uuid.uuid4())
            # email = instance.email
            # User.objects.create(user=instance,email_token=email_token)
            send_account_activation_email(email, email_token)

    except Exception as e:
        print(e)
