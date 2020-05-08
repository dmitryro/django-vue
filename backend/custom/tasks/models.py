from __future__ import unicode_literals

from django.db import models

class TaskLog(models.Model):
    username = models.CharField(max_length=128,blank=True,null=True)
    job = models.CharField(max_length=128,blank=True,null=True)
    show_id = models.IntegerField(blank=True,null=True)
    is_complete = models.BooleanField(default=False) 
    user_id =  models.IntegerField(blank=True,null=True)
    session_key = models.CharField(max_length=200,blank=True,null=True)

    class Meta:
        verbose_name = 'TaskLog'
        verbose_name_plural = 'TaskLogs'
# Create your models here.
