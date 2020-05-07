from rest_framework import serializers
from users.serializers import UserSerializer
from chat.models import Message, UserMessage, Room


class RoomSerializer(serializers.ModelSerializer):
    creator = UserSerializer(many=False, read_only=True)
    
    class Meta:
        model = UserMessage
        fields = ('id', 'creator', 'name', 'time_created',)

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(many=False, read_only=True)
    room = RoomSerializer(many=False, read_only=True)

    class Meta:
        model = UserMessage
        fields = ('id', 'body', 'sender', 'room', 'time_sent',)


class UserMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(many=False, read_only=True)
    receiver = UserSerializer(many=True, read_only=True)

    class Meta:
        model = UserMessage
        fields = ('id', 'body', 'sender', 'receiver', 'time_sent',)
