from pyexpat import model
from statistics import mode
from tabnanny import verbose
from django.db import models
from django.db import models

from main.models import BaseModel
from versatileimagefield.fields import VersatileImageField

# Create your models here.
class Posts(BaseModel):
    post=VersatileImageField(upload_to="posts/",blank=True,null=True)
    user = models.ForeignKey('accounts.Profile',on_delete=models.CASCADE,blank=True,null=True)
    description = models.TextField(blank=True,null=True)

    class Meta:
        db_table = 'users_posts'
        verbose_name='post'
        verbose_name_plural = 'posts'
    
    def __str__(self):
        return self.description

class PostLikes(BaseModel):
    post = models.ForeignKey('posts.Posts',on_delete=models.CASCADE,blank=True,null=True)
    liked_user = models.ForeignKey('accounts.Profile',on_delete=models.CASCADE,blank=True,null=True)

    class Meta:
        db_table='post_likes'
        verbose_name= 'like'
        verbose_name_plural='likes'

    def __str__(self):
        return self.liked_user.name
    

class PostComments(BaseModel):
    comment = models.TextField(blank=True,null=True)
    post = models.ForeignKey('posts.Posts',on_delete=models.CASCADE,blank=True,null=True)
    commented_user=models.ForeignKey('accounts.Profile',on_delete=models.CASCADE,blank=True,null=True)

    class Meta:
        db_table = 'posts_comments'
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def __str__(self):
        return self.comment


class Status(BaseModel):
    status = models.FileField(upload_to='status/',blank=True,null=True)
    user = models.ForeignKey('accounts.Profile',on_delete=models.CASCADE,blank=True,null=True)

    class Meta:
        db_table = 'status',
        verbose_name = 'status'
        verbose_name_plural= 'statuses'

    def __str__(self):
        return self.name