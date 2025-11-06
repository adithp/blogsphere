from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone 


import uuid


class User(models.Model):
    id = models.UUIDField(default=uuid.uuid4,null=False,primary_key=True,editable=False)
    email = models.EmailField(null=False,unique=True)
    name = models.CharField(max_length=35,null=False)
    bio = models.TextField(null=True,blank=True)
    profile_image = models.ImageField(upload_to='profile/',null=True,blank=True)
    is_admin = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    date_joined = models.DateField(auto_now_add=True)
    latest_update = models.DateField(auto_now=True)
    password = models.CharField(max_length=256)
    is_active = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.name
    
    

class UserOtp(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)
    
    
class PasswordReset(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def is_expired(self):
        time = timezone.now() - self.created_at
        return time < timedelta(10)
    