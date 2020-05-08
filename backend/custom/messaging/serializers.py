from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import generics

from models import Message
from models import Notification
from models import NotificationType
from models import MessagingSettings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class NotificationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationType
        fields = ('id','notification_code','notification_type')


class NotificationSerializer(serializers.ModelSerializer):
    notification_type = NotificationTypeSerializer(many=False, read_only=True)

    class Meta:
        model = Notification
        fields = ('id', 'is_received', 'is_sent', 'message',
                  'notification_type', 'user', 'time_sent')


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(many=False, read_only=True)
    receiver = UserSerializer(many=False,read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'title', 'is_seen', 'is_answered', 
                  'body', 'time_sent', 'sender', 'receiver','receiver_name')


class MessagingSettingsSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    
    class Meta:
        model = MessagingSettings
        fields = ('id', 'duplicate_private', 'user',)
 
