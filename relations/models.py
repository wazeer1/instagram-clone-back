from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from notification.models import Notification

from main.models import BaseModel

# Create your models here.
# class Followers(BaseModel):
#     user = models.CharField(max_length=255,blank=True,null=True)
#     followed_user = models.ForeignKey('accounts.Profile',on_delete=models.CASCADE,blank=True,null=True)
#     request_accepted = models.BooleanField(default=False,blank=True,null=True)
#     request_declined = models.BooleanField(default=False,blank=True,null=)

#     class Meta:
#         db_table = 'followers'
#         verbose_name = 'follower'
#         verbose_name_plural = 'followers'

#     def __str__(self):
#         return self.user


class Followers(BaseModel):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    is_accepted = models.BooleanField(default=False, blank=True,null=True)

    class Meta:
        db_table='follow'
        verbose_name='follow'
        verbose_name_plural='follows'

    def __str__(self):
        return self.follower.username