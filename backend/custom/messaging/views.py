from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from restless.views import Endpoint

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework import filters
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from signals import message_read
from signals import message_sent
from signals import message_deleted
from signals import message_updated
from signals import message_duplicate_to_email
from callbacks import message_deleted_handler
from callbacks import message_read_handler
from callbacks import message_sent_handler
from callbacks import message_updated_handler
from callbacks import message_duplicate_to_email_handler
from serializers import MessageSerializer
from serializers import MessagingSettingsSerializer
from serializers import NotificationSerializer
from serializers import NotificationTypeSerializer
from serializers import UserSerializer
from filters import MessagingSettingsFilter
from filters import MessageFilter
from filters import NotificationFilter
from filters import UserFilter
from models import Message
from models import Notification
from models import NotificationType
from models import MessagingSettings
from custom.utils.models import Logger

import logging
logger = logging.getLogger(__name__)

class MessagingSettingsList(generics.ListAPIView):
    queryset = User.objects.all()
    filter_class = MessagingSettingsFilter
    serializer_class = MessagingSettingsSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('duplicate_private',)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', 'email')    


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_class = UserFilter
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'username', 'email')


class MessagingSettingsViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing messaging settings instances.
    """
    filter_class = MessagingSettingsFilter
    serializer_class = MessagingSettingsSerializer
    queryset = MessagingSettings.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'duplicate_private',)


@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def msg_duplication_view(request):
    """
    A view to activate or deactivate private message duplication
    """
    data = JSONParser().parse(request)
    user_id = data['user_id']
    toggle = data['toggle']

    if request.user.is_authenticated():
        user = request.user
    else:
        try:
            user = User.objects.get(id=int(user_id))
        except Exception as e:
            return Response({'resilt':'error'})
  
    try:
        user_id = int(user_id)
        messages_settings = MessagingSettings.objects.get(user=user)
        messages_settings.duplicate_private = bool(toggle)
        messages_settings.save()
        serializer = MessagingSettingsSerializer(messages_settings, many=False)
    except ObjectDoesNotExist:
        messages_settings = MessagingSettings.objects.create(user=user, 
                                                             duplicate_private=bool(toggle))
        serializer = MessagingSettingsSerializer(messages_settings, many=False)
    log = Logger(log='WE ARE RETURNING {}'.format(str(serializer.data)))
    log.save()

    return Response(serializer.data)


@api_view(['POST'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def outgoing_messages_view(request):
    """
     A view that returns outgoing messages
    """
    try:
       data = JSONParser().parse(request)
       user_id = data['sender_id'].encode('utf-8')
       messages_list = Message.objects.filter(sender_id=user_id)
       serializer = MessageSerializer(messages_list, many=True)
    except Exception as e:
       return Response({})
    return Response(serializer.data)    
    

@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def incoming_messages_view(request):
    """
     A view that returns incoming messages
    """
    try:
       data = JSONParser().parse(request)
       user_id = data['receiver_id'].encode('utf-8')
       messages_list = Message.objects.filter(receiver_id=user_id)
       serializer = MessageSerializer(messages_list, many=True)
    except Exception as e:
       log = Logger(log='WE FUCKED IT UP {}'.format(str(e)))
       log.save()
       return {}
    return Response(serializer.data)


class IncomingMessagesList(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer, )

    def get_queryset(self):
        """
        This view should return a list of all the messages
        that are outgoing for the given sender.
        """
        try:
            receiver_id = self.kwargs['receiver_id']
            receiver_id = int(receiver_id)

            return Message.objects.filter(receiver_id=receiver_id)

        except Exception, R:
            receiver_id = self.request.user.id
            return Message.objects.filter(receiver_id=receiver_id)

class OutgoingMessagesList(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer, )

    def get_queryset(self):
        """
        This view should return a list of all the messages
        that are outgoing for the given sender.
        """

        try:
            sender_id = self.kwargs['sender_id']
            sender_id = int(sender_id)
            return Message.objects.filter(sender_id=sender_id)

#            return Message.objects.filter(sender_id=sender_id)
        except Exception, R:
            sender_id = self.request.user.id
            return Message.objects.filter(sender_id=sender_id)

      #      return Message.objects.filter(sender_id=sender_id)
 

class NotificationTypeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing post instances.
    """
    serializer_class = NotificationTypeSerializer
    queryset = NotificationType.objects.all()


class NotificationViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing post instances.
    """
    serializer_class = NotificationSerializer
    filter_class = NotificationFilter
    queryset = Notification.objects.all()

class MessageViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing post instances.
    """
    serializer_class = MessageSerializer
    filter_class = MessageFilter
    queryset = Message.objects.all()
    
class SendMessageView(Endpoint):
    @csrf_exempt
    def get(self, request):
        

        try:

           title = request.params.get('title','')
           body = request.params.get('body','')
           receiver_id = int(unicode(request.params.get('receiver_id')))            
           receiver = User.objects.get(id=receiver_id)
           sender = request.user

           #return {"receiver":receiver.id,"sender":sender.id}

        except Exception as e:
           log = Logger(log="WE FAILED LOUDLY"+str(e))
           log.save()
           return {"message":"error"+str(e)}


        try:
            message = Message.objects.create(title=title,
                                             body=body,
                                             sender=sender,
                                             receiver=receiver)

            messages_list = Message.objects.filter(sender_id=sender.id)

            serializer = MessageSerializer(messages_list, many=True)

            message_sent.send(sender = sender,
                              receiver = receiver,
                              message = message,
                              kwargs = None)

            if receiver.messagingsettings:
                if receiver.messagingsettings.duplicate_private:
                    message_duplicate_to_email.send(sender = sender,
                                                    receiver = receiver,
                                                    message = message,
                                                    kwargs = None)

        except Exception, R:
            log = Logger(log=str(R))
            log.save()

        return {'messages':serializer.data}

    @csrf_exempt
    def post(self, request, *args, **kwargs):

        try:

            log = Logger(log='We will try to send %s'%str(request.data))
            log.save()
            title = request.data.get('title','default title')
            body = request.data.get('body', 'default body')
            try:
                sender_id = int(unicode(request.data.get('sender_id')))
                sender = User.objects.get(id=sender_id)
            except Exception as e:
                sender = request.user

            receiver_id = int(unicode(request.data.get('receiver_id')))
            log = Logger(log='MESSAGE RECEIVER ID %s'%receiver_id)
            log.save()
        except Exception as e:
            log = Logger(log='So far we failed sending message %s'%str(e))
            log.save()

            return {"message":"error"+str(e)}

        try:

           receiver = User.objects.get(id=receiver_id)
           log = Logger(log='BYPASSED ONE')
           log.save()


           #return {"receiver":receiver.id,"sender":sender.id}

        except Exception as e:
           log = Logger(log="WE FAILED LOUDLY TO READ THE RECEIVER "+str(e))
           log.save()
           return {'messages':[]}

        try:
            message = Message.objects.create(title = title,
                                             body = body,
                                             sender = sender,
                                             receiver = receiver)

            messages_list = Message.objects.filter(sender_id=sender.id)

            serializer = MessageSerializer(messages_list, many=True)

            message_sent.send(sender = sender,
                              receiver = receiver,
                              message = message,
                              kwargs = None)
            if receiver.messagingsettings:
                if receiver.messagingsettings.duplicate_private:
                    message_duplicate_to_email.send(sender = sender,
                                                    receiver = receiver,
                                                    message = message,
                                                    kwargs = None)
        
            
        except Exception as e:
            log = Logger(log="We were unable to send message - "+str(e))
            log.save()
            return {'messages':[]}
        
       
        return {'messages':serializer.data}


class DeleteMessageView(Endpoint):
    @csrf_exempt
    def get(self, request):
        try:
            message_id = int(unicode(request.params.get('message_id',0))) 
            log = Logger(log="MESSAGE ID IN GET IS %d"%message_id)
            log.save()


            mode = int(unicode(request.params.get('mode',0)))
            message = Message.objects.get(id=message_id)
            message.delete()
            messages_list = Message.objects.filter(sender_id=request.user.id)

            if mode==1:
                messages_list = Message.objects.filter(sender_id=request.user.id)
            else:
                messages_list = Message.objects.filter(receiver_id=request.user.id)

            serializer = MessageSerializer(messages_list, many=True)
            return {'messages':serializer.data}

        except Exception as e:
            log = Logger(log="SOMETHING BAD HAS HAPPENED IN DELETE GET %s - %s"%(e,request.params))
            log.save()
            return {'messages':'error','exception':'message id is a mandatory'}


    @csrf_exempt
    def post(self, request):
        try:
            message_id = int(unicode(request.data['message_id']))


            log = Logger(log="MESSAGE ID IN POST IS %d"%message_id)
            log.save()

            mode = int(unicode(request.data.get('mode',0)))
            log = Logger(log="MODE IN POST IS %d"%mode)
            log.save()


            message = Message.objects.get(id=message_id)
            message.delete()

            if mode==1:
                messages_list = Message.objects.filter(sender_id=request.user.id)
            else:
                messages_list = Message.objects.filter(receiver_id=request.user.id)

            serializer = MessageSerializer(messages_list, many=True)
            return {'messages':serializer.data}

        except Exception as e:
            log = Logger(log="SOMETHING BAD HAS HAPPENED IN DELETE POST %s %d"%(e,message_id))
            log.save()

            return {'messages':'error','exception':'message id is a mandatory'}


class UpdateMessageView(Endpoint):
    @csrf_exempt
    def get(self, request):
        return {'message':'error','exception':'email is a mandatory'}

    @csrf_exempt
    def post(self, request):
        return {'message':'error','exception':'email is a mandatory'}


class ReadMessageView(Endpoint):

    @csrf_exempt
    def get(self, request):
        user = request.user
        message_id = int(unicode(request.params.get('message_id',0)))


        try:
            message = Message.objects.get(id=message_id)
          

            message.is_seen = True
            message.save()
            messages = Message.objects.filter(receiver=user, is_seen=False)
            total_unseen = len(messages)

            serializer = MessageSerializer(message, many=False)
            message_read.send(sender = message.sender,
                              receiver = user,
                              message = message,
                              kwargs = None)

            return {"messages":serializer.data, "total_unseen": total_unseen}

        except Exception,R:
            log = Logger(log=str(R))
            log.save()
            return {'messages':{'message':'error  '+str(R)}}



    @csrf_exempt
    def post(self, request):
        user = request.user
        message_id = int(unicode(request.data.get('message_id',0)))
        m_id = int(message_id)


        try:
            message = Message.objects.get(id=m_id)

            message.is_seen = True
            message.save()


            messages = Message.objects.filter(receiver=user, is_seen=False)
            total_unseen = len(messages)

            message_read.send(sender = message.sender,
                              receiver = user,
                              message = message,
                              kwargs = None)

            serializer = MessageSerializer(message,many=False)

            return {"messages":serializer.data, "total_unseen": total_unseen}

        except Exception,R:
            log = Logger(log=str(R))
            log.save()
            return {'messages':{'message':'error  '+str(R)}}


@api_view(['POST'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def send_question_view(request):
   
    email = str(request.data.get('email', ''))
    full_name = str(request.data.get('full_name', ''))
    message = request.data['message']
    subject = request.data['subject']

    try:
        serializer = MessageSerializer(message, many=False)
        return Response(serializer.data)
    except Exception as e:
        return None

message_duplicate_to_email.connect(message_duplicate_to_email_handler)
message_read.connect(message_read_handler)
message_sent.connect(message_sent_handler)
message_deleted.connect(message_deleted_handler)
message_updated.connect(message_updated_handler)
