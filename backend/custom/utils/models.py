from __future__ import unicode_literals

from django.db import models



class Logger(models.Model):
    log = models.CharField(max_length=3500,blank=True,null=True)
    time = models.DateTimeField(auto_now_add=True)

