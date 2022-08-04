from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    socialID = models.CharField(max_length=30, null=True)
    socialPW = models.CharField(max_length=20, null=True)
    phoneNumber = models.IntegerField(null=True)
    age = models.IntegerField(null=True)
    nickName = models.CharField(max_length=10, null=True)