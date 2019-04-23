from django.db import models

# Create your models here.
import datetime
import json

from django.db import models

# Create your models here.
from django.utils import timezone


class Need(models.Model):
    user_id = models.IntegerField()
    level = models.IntegerField(default=1)
    category = models.CharField(max_length=100,default='')
    content = models.TextField(default='')
    images = models.TextField(default=json.dumps([]))
    tags = models.TextField(default=json.dumps([]))
    files = models.TextField(default=json.dumps([]))
    quote = models.IntegerField(default=0)
    need_status = models.IntegerField(default=0)
    status = models.IntegerField(default=1)
    ctime = models.DateTimeField(default = timezone.now)
    mtime = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    name = models.CharField(max_length=100)
    status = models.IntegerField(default=1)
    ctime = models.DateTimeField(default = timezone.now)
    mtime = models.DateTimeField(auto_now=True)


class Category(models.Model):
    name = models.CharField(max_length=100)
    status = models.IntegerField(default=1)
    ctime = models.DateTimeField(default = timezone.now)
    mtime = models.DateTimeField(auto_now=True)

