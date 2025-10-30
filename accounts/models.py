from django.db import models
import uuid

# Create your models here.


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
    