import uuid
from django.db import models
from versatileimagefield.fields import VersatileImageField


# Create your models here.
PROFILE_GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('others', 'Others'),
)

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
    # ign = models.CharField(max_length=128, blank=True, null=True)
    # ig_id =  models.CharField(max_length=128, blank=True, null=True)
    user = models.OneToOneField("auth.User",on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    phone = models.CharField(max_length=128, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    gender = models.CharField(max_length=128,choices=PROFILE_GENDER_CHOICES)
    photo = VersatileImageField(upload_to="profile/",blank=True,null=True)
    username = models.CharField(max_length=155,blank=True,null=True)
    password = models.TextField(blank=True, null=True)
    # fireid = models.CharField(default='null',max_length=128, blank=True, null=True)
    
    is_verified = models.BooleanField(default=False)
    is_profile_updated = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    
    gender = models.CharField(max_length=128, choices=PROFILE_GENDER_CHOICES, null=True, blank=True)
    dob = models.DateField(blank=True, null=True)
    

    class Meta:
        db_table = 'users_profile'
        verbose_name ='profile'
        verbose_name_plural ='profiles'
        ordering = ('name',)
        
    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.phone