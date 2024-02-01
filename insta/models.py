from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import datetime as dt
from django.db.models.signals import post_save, post_delete
from cloudinary.models import CloudinaryField
from django.utils import timezone

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
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')
        if email is None:
            raise TypeError('Superusers must have an email.')
        if username is None:
            raise TypeError('Superusers must have an username.')
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.email = email
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(default=dt.datetime.now)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    password = models.CharField(max_length=100)
    last_seen = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    image = CloudinaryField("image")
    captions = models.TextField()
    created_time = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    saved = models.BooleanField(default=False)
    location = models.CharField(max_length=60, blank=True)


    def __str__(self):
        return self.captions
    
    
    
class CarouselImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = CloudinaryField("image")

    def __str__(self):
        return f"Carousel Image for {self.post}"


class Profile(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100, null=True, default='')
    photo = CloudinaryField("photo")
    bio = models.CharField(max_length=280)
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=OTHER,
    )

    def __str__(self):
        return f"{self.user} Profile"

    def save_profile(self):
        self.save()


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=False)



class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE, null=True)

    
    class Meta:
        unique_together = ('follower', 'following')  # Each follow instance should be unique

    def __str__(self):
        return f"{self.follower} follows {self.following}"
    

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)