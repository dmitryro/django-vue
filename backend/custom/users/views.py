from datetime import datetime
import logging
from .models import User
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import filters, generics, viewsets, mixins
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from users.serializers import UserSerializer
from rest_framework import permissions


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def auth_user(request):
    return Response({"message": "success",
                     "status": "posted",
                     "code": 200,
                     "falure_code": 0}, status=200)


class CreateUserView(CreateAPIView):

    model = get_user_model()
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'first_name', 'last_name', 'email', "username"]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        obj = []

        return obj
 
 
    def post(self, request, *args, **kwargs):
        username = request.data.get("username", None)
        first_name = request.data.get("first_name", None)
        last_name = request.data.get("last_name", None)
        email = request.data.get("email", None)
        
        User.objects.create(username=username, 
                            first_name=first_name, 
                            last_name=last_name, 
                            email=email)
        return self.list(request, *args, **kwargs)

