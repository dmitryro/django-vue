from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
import django.contrib.auth as auth


from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from restless.views import Endpoint
from custom.users.models import Contact
from custom.utils.models import Logger
from custom.users.models import Profile
from custom.users.models import MileStone
from custom.users.models import Advantage
from custom.users.models import AdvantageLink
from custom.users.models import Profile
from custom.gui.models import Slide
from custom.gui.models import Service
from custom.gui.models import FAQ
from custom.gui.models import QualifyQuestion
from custom.gui.models import QualifyQuestionnaire
from custom.blog.models import Category
from custom.blog.models import Post
from custom.messaging.models import Message
from custom.messaging.signals import message_sent
from custom.messaging.signals import message_duplicate_to_email
from custom.messaging.callbacks import message_sent_handler
from custom.messaging.callbacks import message_duplicate_to_email_handler

from signals import user_send_email
from callbacks import  user_send_email_handler



####################################
## Subscribe News Letter Endpoint ##
## METHOD : GET, POST ##############
## RETURNED: SUCCESS/FAILUTRE ######
####################################

class SendEmailView(Endpoint):

    @csrf_exempt
    def get(self, request):
        try:
           email = request.params.get('email','')     
           if not email or len(email) < 1:
              return {'message':'error','exception':'email is a mandatory'}

           message = request.params.get('message','')

           if not message or len(message) < 1:
              return {'message':'error','exception':'message is a mandatory'}


           phone = request.params.get('phone','')
           subject = request.params.get('subject','')
           name = request.params.get('name','')
           if not name or len(name) < 1:
              return {'message':'error','exception':'name is a mandatory'}

           contact = Contact.objects.create(name=name,
                                            email=email,
                                            message=message, 
                                            subject=subject, 
                                            phone=phone)
           user_send_email.send(sender=User, contact=contact, kwargs=None)
           log = Logger(log='WE ARE SENDING EMAIL IN GET '+email)
           log.save()
           return {'message':'success','s3_base_url':"blablabla"}
        except Exception, R:
           log = Logger(log='WE HAD AN ERROR '+str(R))
           log.save()   
           return {'message':'error','data':'we failed reading s3 base url'}

    @csrf_exempt
    def post(self, request):
        try:  

           email =  request.data['email']
           log = Logger(log='WE ARE SENDING EMAIL'+str(email))
           log.save()
           return {'message':'success','s3_base_url':"blablabla"}
        except Exception, R:
           return {'message':'error','data':'we failed reading s3 base url'}


####################################
## Subscribe News Letter Endpoint ##
## METHOD : GET, POST ##############
## RETURNED: SUCCESS/FAILUTRE ######
####################################

class SubscribeView(Endpoint):
    @csrf_exempt
    def get(self, request):  # Get requests handler
        try:
           email = request.params.get('email','')

           try:
               contact = Contact.objects.get(email=email)
           except Exception as R:
               contact = Contact.objects.create(email=email)

           return {'message' : 'success', 'email' : email}

        except Exception as R:

           return {'message':'error','data':'we failed reading s3 base url'}

    @csrf_exempt
    def post(self, request): # Post requests handler
        try:

           email =  request.data['email']

           contact = Contact.objects.filter(email=email)
           log = Logger(log="SO FAR FOUND EMAILS"+str(len(contact)))
           log.save()
 
           if len(contact)<1:
               contact = Contact.objects.create(email=email)
               

           return {'message':'success','email':email}

        except Exception, R:

           return {'message':'error','data':'we failed reading s3 base url'}

@csrf_exempt
def activate(request, activation_key):
    milestones = MileStone.objects.all()
    advantage_links = AdvantageLink.objects.filter(advantage_id=1)
    slides = Slide.objects.all()
    faqs = FAQ.objects.all()
    posts = post = Post.objects.all()
    qquestions = QualifyQuestion.objects.all()

    if request.user.is_authenticated():
        logout=True
        try:
           user_id = request.user.id
           username = request.user.username
           first_name = request.user.first_name
           last_name = request.user.last_name
           profile_image_path = ''
        except Exception, R:
           log = Logger(log='WE GOT SOME ERROR'+str(R))
           log.save()
           user_id = -1
           username = ''
           first_name = ''
           last_name = ''
           profile_image_path = ''
        HttpResponseRedirect('/dashboard')
    else:
        user_id = -1
        logout=False
        username = ''
        first_name = ''
        last_name = ''
        profile_image_path = ''


    # check if there is UserProfile which matches the activation key (if not then display 404)

        #user = User.objects.get(id=user_profile.id)
    try:
        user_profile = Profile.objects.get(activation_key=activation_key)
        usr = User.objects.get(id=user_profile.id) 
        usr.backend = 'django.contrib.auth.backends.ModelBackend'
        auth.login(request, usr)
    
        usr.is_active=True
        usr.save()
        logout = True
     #   ip = get_real_ip(request, right_most_proxy=True)

#        usr.profile.ipaddress=str(ip)
    except Exception as e:
        return render(request, 'index-0.html', {'home': 'index-0.html', 'link_expired':1, 'error':'expired'})

    try:
        if not usr.profile.is_activated:
            usr.profile.is_activated = True
            usr.profile.activation_sent = True
            usr.profile.is_new = 0
            usr.profile.is_cleared = 1
            usr.profile.activation_key = None
            usr.profile.save()
            
            message_title = 'Welecome to Grinberg and Segal'
            message_body = 'Dear {} {}! We are glad to see you here!'.format(usr.first_name,
                                                                             usr.last_name)

            attorney = User.objects.get(id=14)
            message = Message.objects.create(title=message_title,
                                             body=message_body,
                                             sender=attorney,
                                             receiver=usr)

            message_sent.send(sender = attorney,
                              receiver = usr,
                              message = message,
                              kwargs = None)

            message_duplicate_to_email.send(sender = attorney,
                                            receiver = usr,
                                            message = message,
                                            kwargs = None)



    
       # new_user_cleared.send(sender=usr, instance = usr, kwargs=None) 
        return render(request, 'index-0.html',{'logout':logout,
                                                 'user_id':user_id,
                                                 'first':first_name,
                                                 'last':last_name,
                                                 'is_activated': 1,
                                                 'link_expired': 0,
                                                 'slides':slides,
                                                 'faqs':faqs,
                                                 'qualifying':qquestions,
                                                 'posts':posts,
                                                 'milestones':milestones,
                                                 'advantage_links':advantage_links,
                                                 'profile_image':profile_image_path})


    except Exception as R:
        log = Logger(log='ERROR ACTIVATING USER '+str(R))
        log.save()
        #usr.profile.is_new = 1
        #usr.profile.is_cleared = 0
        #usr.profile.save()
        
        return render(request, 'index-0.html', {'home': 'index-0.html', 'link_expired': 1,'error':'expired'})

    return render(request, 'index-0.html',{'logout':logout,
                                           'user_id':user_id,
                                           'first':first_name,
                                           'last':last_name,
                                           'slides':slides,
                                           'faqs':faqs,
                                           'qualifying':qquestions,
                                           'posts':posts,
                                           'milestones':milestones,
                                           'advantage_links':advantage_links,
                                           'profile_image':profile_image_path})



@csrf_exempt
def confirm(request):
    return render(request, 'confirm.html',{})
 
@csrf_exempt
def logout_view(request):
    logout(request)


message_duplicate_to_email.connect(message_duplicate_to_email_handler)
user_send_email.connect(user_send_email_handler)
message_sent.connect(message_sent_handler)
