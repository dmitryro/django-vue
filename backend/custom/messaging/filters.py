from django.contrib.auth.models import User
import rest_framework_filters as filters

from models import Notification
from models import Message
from models import MessagingSettings


class MessagingSettingsFilter(filters.FilterSet):
    user_id = filters.CharFilter(name='user_id')
    duplicate_private = filters.BooleanFilter(name='duplicate_private')
    class Meta:
        model = MessagingSettings
        fields = ['id', 'duplicate_private', 'user_id']


class UserFilter(filters.FilterSet):
    email = filters.CharFilter(name='email')
    username = filters.CharFilter(name='username')
    first_name = filters.CharFilter(name='first_name')
    last_name = filters.CharFilter(name='last_name')

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email',]


class MessageFilter(filters.FilterSet):
#    is_seen = filters.CharFilter(name='is_seen')
#    is_answered = filters.CharFilter(name='is_answered')
#    title = filters.CharFilter(name='title')
#    body = filters.CharFilter(name='body')
#    receiver = filters.CharFilter(name='receiver') 
#    sender = filters.CharFilter(name='sender')
#    time_sent = filters.CharFilter(name='time_sent')

    class Meta:
        model = Message
        fields = ['is_seen', 'is_answered', 'title', 'body', 'receiver', 'sender', 'time_sent']
      #       'is_seen': [''] #,i 'is_answered', 'title', 'body', 'receiver', 'sender', 'time_sent'],
      #  }


class NotificationFilter(filters.FilterSet):
#    is_received = filters.CharFilter(name='is_received')
#    is_sent = filters.CharFilter(name='is_sent')
#    notification_type = filters.CharFilter(name='notification_type')
#    user = filters.CharFilter(name='user')
#    time_sent = filters.CharFilter(name='time_sent')

    class Meta:
        model = Notification
        fields = ['is_received', 'is_sent', 'notification_type', 'user', 'time_sent']

       
