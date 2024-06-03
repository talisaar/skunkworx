from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class myUser(User):
    username = User.email

class Post(models.Model):
    owner = models.ForeignKey('myUser', related_name='posts', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=140, blank=True, default='')
    title = models.CharField(max_length=140, blank=True, default='default title')