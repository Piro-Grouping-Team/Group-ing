from turtle import back
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, username, name, password):
        if not email:
            raise ValueError('must have user email')
        if not username:
            raise ValueError('Users must have an userID')
        if not password:
            raise ValueError('must have user password')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            name = name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, name, password):   
   
       user = self.create_user(            
           email = self.normalize_email(email),    
           username = username,
           name = name,                 
           password=password,     
       )
       user.is_admin = True
       user.is_superuser = True
       user.save(using=self._db)
       return user 
       
# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    email = models.EmailField(        
       max_length=255,
       verbose_name='이메일',
       unique=True,    
    )
    username = models.CharField(
        max_length=20,  
        unique=True,
    )
    name = models.CharField(max_length=20, null=False, blank=False, verbose_name='이름')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username' #로그인 ID로 사용할 필드
    REQUIRED_FIELDS = ['email', 'name'] #필수 작성 필드
    def __str__(self):
        return self.username
    
    @property
    def is_staff(self):
       return self.is_admin
# class User(AbstractBaseUser, PermissionsMixin):
#     GENDER_CHOICES = (
#         ('male', '남성'),
#         ('female', '여성'),
#         ('none', '선택안함')
#     )
#     socialID = models.CharField(max_length=30, null=True)
#     socialPW = models.CharField(max_length=20, null=True)
#     phoneNumber = models.IntegerField(null=True)
#     gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
#     age = models.IntegerField(null=True)
#     nickName = models.CharField(max_length=10, null=True)
#     intro = models.CharField(max_length=100, null=True)