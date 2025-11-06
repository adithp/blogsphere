from django.db import models
from datetime import datetime, timedelta

from ckeditor_uploader.fields import RichTextUploadingField
from autoslug import AutoSlugField

from accounts.models import User


class BaseModel(models.Model):
    created = models.DateField(auto_now_add=True,null=True)
    updated = models.DateField(auto_now=True,null=True)
    
    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=25,null=False,blank=False,unique=True)
    
    
    class Meta:
        db_table = 'categories'
        
    def __str__(self):
        return self.title


class Post(BaseModel):
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    title = models.CharField(max_length=150)
    content = RichTextUploadingField()
    thumbnail = models.ImageField(upload_to='thumbnail/')
    slug = AutoSlugField(unique=True,populate_from='title')
    is_archived = models.BooleanField(default=False)
    likes_count = models.IntegerField(default=0)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    comment_count = models.IntegerField(default=0)
    
    
    def __str__(self):
        return self.slug
    
    class Meta:
        db_table = 'posts'
        
class LatestPost(Post):
    
    class Meta:
        proxy = True
        ordering = ['-updated']
    
    
class BaseFunctionModel(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    
    class Meta:
        abstract = True
    

class PostLike(BaseFunctionModel):
    pass


    class Meta:
        db_table = 'post_likes'


class Comment(BaseFunctionModel):
    content = models.TextField()
    is_deleted = models.BooleanField(default=False)
    
    
    class Meta:
        db_table = 'post_comments'
    
    
