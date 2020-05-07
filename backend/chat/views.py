#from django_chatter.views import chatroom
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes, parser_classes
from chat.serializers import UserMessageSerializer, MessageSerializer, RoomSerializer
from users.models import User

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated,])
@parser_classes([JSONParser,])
@authentication_classes([JSONWebTokenAuthentication,])
@renderer_classes((JSONRenderer,))
def direct_chat_view(request):
    if request.method == 'GET':
        return Response({"message":"success"})

    if request.method == 'POST':
        message = request.data.get('message', '')
        room_id = request.data.get('room_id', '')
        user1_id = request.data.get('user1_id', '') 
        user2_id = request.data.get('user2_id', '')
        #user1 = request.user  # User requesting the view

        #user2 = User.objects.get(username="user2")  # example user in your db
        #room_id = create_room([user1, user2])
        #return chatroom(request, room_id)
        return Response({"message": "success", "message":message, "user1_id":user1_id, "user2_id": user2_id, "room_id": room_id})


    if request.method == 'DELETE':
        return Response({"message": "success"})


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated,])
@parser_classes([JSONParser,])
@authentication_classes([JSONWebTokenAuthentication,])
@renderer_classes((JSONRenderer,))
def group_chat_view(request):
    if request.method == 'GET':
        return Response({"message":"success"})

    if request.method == 'POST':
        message = request.data.get('message', '')
        room_id = request.data.get('room_id', '')
        return Response({"message": "success", "message": message, "room_id": room_id})

    if request.method == 'DELETE':
        return Response({"message": "success"})
