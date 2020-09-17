from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from django.core.validators import FileExtensionValidator
import pytz

utc=pytz.UTC

# Create your models here.
class Users(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=191, unique=True)
    username = models.CharField(max_length=191, unique=True, blank=True, null=True)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    age = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    weight = models.FloatField(max_length=10, blank=True, null=True)
    profile_img = models.ImageField(blank=True, null=True, default="default_avatar.png")
    is_active = models.BooleanField(blank=True, null=True, default=True)
    slug_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.full_name

class Test(models.Model):
    Jitter_percentage = models.FloatField(max_length=10, null=True)
    Jitter_absolute = models.FloatField(max_length=10, null=True)
    Jitter_ddp = models.FloatField(max_length=10, null=True)
    mdvp_ppq = models.FloatField(max_length=10, null=True)
    mdvp_rap = models.FloatField(max_length=10, null=True)
    mdvp_shimmer = models.FloatField(max_length=10, null=True)
    mdvp_shimmer_db = models.FloatField(max_length=10, null=True)
    shimmer_apq3 = models.FloatField(max_length=10, null=True)
    shimmer_apq5 = models.FloatField(max_length=10, null=True)
    mdvp_avq = models.FloatField(max_length=10, null=True)
    shimmer_dda = models.FloatField(max_length=10, null=True)
    rpde = models.FloatField(max_length=10, null=True)
    d2 = models.FloatField(max_length=10, null=True)
    nhr = models.FloatField(max_length=10, null=True)
    spread_2 = models.FloatField(max_length=10, null=True)
    ppe = models.FloatField(max_length=10, null=True)    
    test_date = models.DateTimeField(default=datetime.now)
    result = models.IntegerField(null=True)
    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE
    )

    # def __str__(self):
    #     return self.title

    def older_than_today(self):
        today = datetime.now()
        post_date = self.test_date
        # # today = today.replace(tzinfo=utc)
        # # post_date = post_date.replace(tzinfo=utc)
        # post_date = post_date.replace(tzinfo=None)
        return (today - post_date).days >= 1

    def older_than_seven_days(self):
        today = datetime.now()
        post_date = self.test_date
        # today = today.replace(tzinfo=utc)
        # post_date = post_date.replace(tzinfo=utc)
        # post_date = post_date.replace(tzinfo=None)
        return (today - post_date).days > 7


class Topic(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE
    )