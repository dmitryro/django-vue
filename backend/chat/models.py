"""
Create models for chat
"""
from django.db import models
from users.models import User

class Room(models.Model):
    creator = models.ForeignKey(User,
                                blank=True,
                                null=True,
                                related_name='creator',
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=250, blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

    def __str__(self):
        return self.name    


class Message(models.Model):
    room = models.ForeignKey(Room,
                             blank=True,
                             null=True,
                             related_name='room',
                             on_delete=models.CASCADE)

    body = models.TextField(blank=True,
                            null=True)

    time_sent = models.DateTimeField(auto_now_add=True)

    sender = models.ForeignKey(User,
                               blank=True,
                               null=True,
                               related_name='message_sender',
                               on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return self.body


class UserMessage(models.Model):
    receiver = models.ForeignKey(User,
                                 blank=True,
                                 null=True,
                                 related_name='user_message_receiver',
                                 on_delete=models.CASCADE)
    body = models.TextField(blank=True,
                            null=True)    
    time_sent = models.DateTimeField(auto_now_add=True)

    sender = models.ForeignKey(User,
                               blank=True,
                               null=True,
                               related_name='user_message_sender',
                               on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'User Message',
        verbose_name_plural = 'User Messages'

    def __str__(self):
        return self.body

