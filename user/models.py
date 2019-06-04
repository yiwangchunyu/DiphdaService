import datetime
import json

from django.db import models

# Create your models here.
from django.utils import timezone


class User(models.Model):
    openid = models.CharField(max_length=100,unique=True)
    username = models.CharField(max_length=100,default='')
    gender = models.IntegerField(default=1)
    avatar = models.CharField(max_length=200,default='')
    tags = models.TextField(default=json.dumps([]))
    level = models.IntegerField(default=0)
    contact_type = models.CharField(max_length=100,default='',blank=True,null=True)
    contact = models.CharField(max_length=100,default='', blank=True, null=True)
    status = models.IntegerField(default=1)
    ctime = models.DateTimeField(default = timezone.now)
    mtime = models.DateTimeField(auto_now=True)

class Tag(models.Model):
    name = models.CharField(max_length=100)
    status = models.IntegerField(default=1)
    ctime = models.DateTimeField(default = timezone.now)
    mtime = models.DateTimeField(auto_now=True)