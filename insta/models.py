from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import datetime as dt
from django.db.models.signals import post_save, post_delete
from cloudinary.models import CloudinaryField
from django.utils import timezone
from django.conf import settings 
# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError(" User must have an email address")
        if not username:
            raise ValueError(" User must have an username!")    
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password = password,
            username=username,
        )
        user.email = email
        user.is_admin = True 
        user.is_staff = True 
        user.is_superuser = True 
        user.save(using=self._db)
        return user
        

class Users(AbstractBaseUser):
    username = models.CharField( max_length=20, unique=True)  
    email = models.CharField( max_length=50, unique=True)    
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(default=dt.datetime.now)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    password = models.CharField( max_length=100)
    
    USERNAME_FIELD = 'email'
        
    objects=MyAccountManager()
     
    def _str_(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
class Post(models.Model):
    author = models.ForeignKey('Users', on_delete=models.CASCADE)
    image = CloudinaryField('image', default='')
    captions = models.TextField()
    created_time = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_likes')
    saved   = models.BooleanField(default=False)
    location = models.CharField(max_length=60, blank=True)  
    
def __str__(self):
    return self.captions

class Profile(models.Model):
    author = models.ForeignKey('Users',  on_delete=models.CASCADE)
    pic = CloudinaryField('pic', default='user.png')
    bio = models.CharField(max_length=280)
    gender= models.CharField(max_length=7)
    
def __str__(self):
    return f'{self.author} Profile'
 
def save_profile(self):
    self.save()
    
    
class Follow(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return self.follower
    
    
    def delete_profile(self):
        self.delete()