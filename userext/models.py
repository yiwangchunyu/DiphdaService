import datetime
import json

from django.db import models

# Create your models here.
from django.utils import timezone


class Userext(models.Model):
    user_id = models.IntegerField()
    expc = models.IntegerField(default=0)
    coin = models.IntegerField(default=0)
    status = models.IntegerField(default=1)
    ctime = models.DateTimeField(default = timezone.now)
    mtime = models.DateTimeField(auto_now=True)
