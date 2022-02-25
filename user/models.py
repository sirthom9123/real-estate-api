from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        email = email.lower()
        
        user = self.model(email=email, username=username)
        
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_realtor(self, email, username, password=None):
        user = self.create_user(email, username, password)    
        
        user.is_realtor = True
        user.save(using=self._db)
        
        return user

    
    def create_superuser(self, email, username, password=None):
        user = self.create_user(email, username, password)
        
        user.is_superuser = True
        user.is_staff = True
        
        user.save(using=self._db)
        
        return user

class UserAccount(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    is_realtor = models.BooleanField(default=True)
    
    objects = UserAccountManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
