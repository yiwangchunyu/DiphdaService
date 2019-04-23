import datetime
import json

from django.db import models

# Create your models here.
from django.utils import timezone


class User(models.Model):
    openid = models.CharField(max_length=100,unique=True)
    username = models.CharField(max_length=100,default='')
    avatar = models.CharField(max_length=200,default='')
    tags = models.TextField(default=json.dumps([]))
    status = models.IntegerField(default=1)
    ctime = models.DateTimeField(default = timezone.now)
    mtime = models.DateTimeField(auto_now=True)