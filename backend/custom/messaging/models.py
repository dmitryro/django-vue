from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    is_seen = models.NullBooleanField(default=False,
                                      blank=True,
                                      null=True)
    is_answered = models.NullBooleanField(default=False,
                                          blank=True,
                                          null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    body = models.CharField(max_length=1000, blank=True, null=True)
    time_sent = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, related_name='sender',
                               db_column="sender",
                               blank=True, null=True)
    receiver = models.ForeignKey(User, related_name='receiver',
                                 db_column="receiver",
                                 blank=True, null=True)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return self.title

    def __unicode__(self):
        return unicode(self.title)

    @property
    def receiver_name(self):
        return self.receiver.first_name+' '+self.receiver.last_name


class NotificationType(models.Model):
    notification_type = models.CharField(max_length=50, blank=True, null=True)
    notification_code = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'Notification Type'
        verbose_name_plural = 'Notification Types'


class Notification(models.Model):
    is_received = models.NullBooleanField(default=False,
                                          blank=True,
                                          null=True)

    is_sent = models.NullBooleanField(default=False,
                                      blank=True,
                                      null=True)

    message =  models.ForeignKey(Message, blank=True, null=True)

    notification_type = models.ForeignKey(NotificationType,
                                          blank=True, null=True)

    user = models.ForeignKey(User, blank=True, null=True)
    time_sent = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'


class MessagingSettings(models.Model):
    user = models.OneToOneField(User, blank=True, null=True) 
    duplicate_private = models.NullBooleanField(default=False,
                                                blank=True,
                                                null=True)

    class Meta:
        verbose_name = 'Messaging Settings'
        verbose_name_plural = 'Messaging Settings'
 
