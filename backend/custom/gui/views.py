from __future__ import absolute_import  # Python 2 only
from jinja2 import Environment
import json
import itertools
import logging
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.contrib.auth import logout as log_out
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib import messages
from django.forms.formsets import formset_factory
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from custom.utils.models import Logger
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.base import View

from custom.users.models import MileStone
from custom.users.models import Advantage
from custom.users.models import AdvantageLink
from custom.gui.models import AskTemplate
from custom.gui.models import Country
from custom.users.models import Profile
from custom.gui.models import ConsultationType
from custom.gui.models import ConsultTemplate
from custom.gui.filters import ServiceFilter
from custom.gui.models import Slide
from custom.gui.models import Service
from custom.gui.models import FAQ
from custom.gui.models import QualifyQuestion
from custom.gui.models import QualifyQuestionnaire
from custom.blog.models import Category
from custom.blog.models import Post
from custom.messaging.models import Message
from custom.messaging.signals import message_sent
from custom.messaging.callbacks import message_sent_handler
from custom.signup.callbacks import resend_activation_handler
from custom.signup.signals import user_resend_activation
from custom.users.models import StateProvince

from rest_framework import filters
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework import generics
from restless.views import Endpoint

from custom.gui.serializers import FrontBlockSerializer
from custom.gui.serializers import CountrySerializer
from custom.gui.serializers import AskTemplateSerializer
from custom.gui.serializers import ConsultationTypeSerializer
from custom.gui.serializers import GlobalSearchSerializer
from custom.gui.serializers import ServiceSerializer
from custom.blog.serializers import CategorySerializer

class CountryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing countries
    """
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    filter_fields = ('id', 'name', 'code',)


class ConsultationTypeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing consultation types
    """
    serializer_class = ConsultationTypeSerializer
    queryset = ConsultationType.objects.all()
    filter_fields = ('id', 'price', 'title', 'description',)


class AskTemplateViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing ask templates
    """
    serializer_class = AskTemplateSerializer
    queryset = AskTemplate.objects.all()
    filter_fields = ('id', 'ask_intro', 'agreement', 'disclaimer',)


class ServiceViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing services
    """
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    filter_class = ServiceFilter
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'title', 'statement', 'time_published', 'description',)


class FAQViewSet(viewsets.ModelViewSet):
    pass



@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
@csrf_exempt
def resend_activation_view(request):
    """
     A view that returns incoming messages
    """
    try:
       data = JSONParser().parse(request)
       user_id = data['user_id'].encode('utf-8')
       if user_id:
           user = User.objects.get(id=int(user_id))
       else:
           user = request.user
       user_resend_activation.send(sender = user,
                                   instance = user,
                                   kwargs = None)

       log = Logger(log='WE VE RESENT THE ACTIVATION')
       log.save()
    except Exception as e:
       log = Logger(log='WE FAILED TO RESEND THE ACTIVATION {}'.format(e))
       log.save()
       return Response({'resent':False})

    return Response({'resent':True})


@api_view(['POST','GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
#@csrf_exempt
def confirm_account_view(request):
    """
     A view that confirms the user
    """
    try:
 #      data = json.loads(request.body).encode('utf-8')
       data = JSONParser().parse(request)
       
       user_id = data['user_id'].encode('utf-8')
       username = data['username'].encode('utf-8')
       first = data['first'].encode('utf-8')
       last = data['last'].encode('utf-8')
       phone = data['phone'].encode('utf-8')
       email = data['email'].encode('utf-8')

       if email:
           users_email = User.objects.filter(~Q(id = int(user_id)), email=email)
       else:
           users_email = []

       if phone:
           users_phone = Profile.objects.filter(~Q(id = int(user_id)), phone=phone)       
       else:
           users_phone = []

       if username:
           users_username = Profile.objects.filter(~Q(id = int(user_id)), username=username)
       else:
           users_username = []

       content = None

       if not phone:
           content = {'user_activated': False,
                      'user_confirmed': False,
                      'error': {'phone':'phone empty'}}

       if not email:
           content = {'user_activated': False,
                      'user_confirmed': False,
                      'error': {'email':'email empty'}}

 
       if len(users_email) > 0:
           content = {'user_activated': False,
                      'user_confirmed': False,
                      'error': {'email':'already used'}}

       if len(users_phone) > 0:
           if not content:
               content = {}
               content['user_confirmed'] = False
               content['user_activated'] = False
           if content.get('error') == None:
               content['error'] = {}
           content['error']['phone']='already used'

       if len(users_username) > 0:
           if not content:
               content = {}
               content['user_confirmed'] = False
               content['user_activated'] = False
           if content.get('error') == None:
               content['error'] = {}
           content['error']['username']='already used'
            

       if content and len(content) > 0 :
           log = Logger(log="WE GOT ERRORS {}".format(content))
           log.save()
           return Response(content)



       user = User.objects.get(id=int(user_id))
       user.is_active = True
       user.profile.is_confirmed = True
       user.profile.is_activated = False
       user.first_name = first
       user.last_name = last
       user.profile.first_name = first
       user.profile.last_name = last
       user.profile.email = email
       user.email = email
       user.profile.phone = phone
       user.username = username
       user.profile.username = username
       user.profile.save()
       user.save()

       user_resend_activation.send(sender = user, 
                                   instance = user,
                                   kwargs = None)

    except Exception as e:
       first = ''
       last = ''
       phone = ''
       email = ''
       username = ''
       user_id = ''
       content = {'user_activated': False, 
                 'error': str(e), 
                 'last': '',
                 'first':''}

              
       log = Logger(log='FAILED TO CONFIRM {}'.format(e))
       log.save()
    
    content = {'user_activated': False,
               'user_confirmed': True, 
               'first': first, 
               'last': last, 
               'phone': phone, 
               'email': email,
               'username': username,
               'user_id': user_id}

    user = User.objects.get(id=user_id)
    user.profile.email = email
    user.email = email
    user.profile.phone = phone
    user.username = username
    user.profile.username = username
    user.profile.save()
    user.save()

    try:
        log_out(request)
    except Exception as e:
        log = Logger(log='FAILED TO LOG OUT {}'.format(e))
        log.save()

    return Response(content)


############################################
## Add a New Post view                    ##
## Extends: restless Endpoint             ##
## METHOD:  GET, POST                     ##
## Type:    Endpoint View (JSON)          ##
############################################

class GetSearchResultsView(Endpoint):
    @csrf_exempt
    def get(self, request):

        try:
            query = request.params.get('q','')

            categories = Category.objects.filter(Q(name__icontains=query) | 
                                                 Q(code__icontains=query))


            services = Service.objects.filter(Q(description__icontains=query) | 
                                              Q(statement__icontains=query) | 
                                              Q(title__icontains=query) | 
                                              Q(service__icontains=query))

            posts = Post.objects.filter(Q(title__icontains=query) | 
                                        Q(body__icontains=query))
        #    res = chain(posts,categories)

            all_results = list(posts)

            serializer_categories = CategorySerializer(categories, many=True)
            serializer_services = ServiceSerializer(services, many=True)
            serializer_posts = GlobalSearchSerializer(posts, many=True)
                               
            return { 'posts': serializer_posts.data,
                     'services': serializer_services.data,
                     'categories':serializer_categories.data,
                     'q':query }

        except Exception,R:
            return {'message':'error '+str(R)}


    @csrf_exempt
    def post(self, request):


        try:

            query = request.data['q']
            categories = Category.objects.filter(Q(name__icontains=query) | 
                                                 Q(code__icontains=query))

            services = Service.objects.filter(Q(description__icontains=query) | 
                                              Q(statement__icontains=query) | 
                                              Q(title__icontains=query) | 
                                              Q(service__icontains=query))

            posts = Post.objects.filter(Q(title__icontains=query) | 
                                        Q(body__icontains=query))
        #    res = chain(posts,categories)
            all_results = list(posts)
            serializer_categories = CategorySerializer(categories,many=True)
            serializer_services = ServiceSerializer(services,many=True)
            serializer_posts = GlobalSearchSerializer(posts,many=True)

            return {'posts':serializer_posts.data,
                    'services':serializer_services.data,
                    'categories':serializer_categories.data,
                    'q':query}


        except Exception,R:

            log = Logger(log=str(R))
            log.save()
            return {'message':'error  '+str(R)}


class GlobalSearchList(generics.ListAPIView):
   serializer_class = GlobalSearchSerializer

   def get_queryset(self):
      query = self.request.QUERY_PARAMS.get('query', None)
      posts = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query) | Q(category__icontains=query))
      users = User.objects.filter(username__icontains=query)
      all_results = list(chain(posts, users)) 
      all_results.sort(key=lambda x: x.created)
      return all_results


@csrf_exempt
def environment(**options):
    env = Environment(**options)
    env.globals.update({
       'static': staticfiles_storage.url,
       'url': reverse,
    })
    return env

@csrf_exempt
def index(request):
    return render(request, 'index.html',{'home':'index.html'})


@csrf_exempt
def dashboard(request):
    
    milestones = MileStone.objects.all()
    advantage_links = AdvantageLink.objects.filter(advantage_id=1)
    slides = Slide.objects.all()
    faqs = FAQ.objects.all()
    posts = Post.objects.all()
    qquestions = QualifyQuestion.objects.all()
    categories = Category.objects.all()
    states = StateProvince.objects.all()

    if request.user.is_authenticated():
        logout=True

        try:
           user_id = request.user.id
           username = request.user.username
           first_name = request.user.first_name
           last_name = request.user.last_name
           profile_image_path = ''
           logging.info("Loading dashboard")
        except Exception as e:
           logging.error("Error loading dashboard {0}".format(e))
           log = Logger(log='WE GOT SOME ERROR'+str(e))
           log.save()
           user_id = -1
           username = ''
           first_name = ''
           last_name = ''
           profile_image_path = ''

        if not request.user.profile.is_activated:
            return render(request, 'index-0.html',{'logout':logout,
                                                   'user_id':user_id,
                                                   'first':first_name,
                                                   'last':last_name,
                                                   'slides':slides,
                                                   'faqs':faqs,
                                                   'posts':posts,
                                                   'qualifying':qquestions,
                                                   'milestones':milestones,
                                                   'advantage_links':advantage_links,
                                                   'profile_image':""})# profile_image_path})

    else:

        user_id = -1
        logout=False
        username = ''
        first_name = ''
        last_name = ''
        profile_image_path = ''
        

        return render(request, 'index-0.html',{'logout':logout,
                                               'user_id':user_id,
                                               'first':first_name,
                                               'last':last_name,
                                               'slides':slides,
                                               'faqs':faqs,
                                               'posts':posts,
                                               'qualifying':qquestions,
                                               'milestones':milestones,
                                               'advantage_links':advantage_links,
                                               'profile_image':""})# profile_image_path})

    
    try:
        messages = Message.objects.filter(receiver_id=user_id, is_seen=False) 
        total_unseen = len(messages)
        log = Logger(log='total unseen is %d'%total_unseen)
        log.save()
    except Exception as e:
        total_unseen = 0
        log = Logger(log='Failed on total unseen  %s'%str(e))
        log.save()


    return render(request, 'dashboard.html',{'logout':logout,
                                           'user_id':user_id,
                                           'first':first_name,
                                           'last':last_name,
                                           'states': states,
                                           'slides':slides,
                                           'faqs':faqs,
                                           'total_unseen': total_unseen,
                                           'qualifying':qquestions,
                                           'posts':posts,
                                           'categories':categories,
                                           'milestones':milestones,
                                           'advantage_links':advantage_links,
                                           'profile_image':profile_image_path})



@csrf_exempt
def home(request):
    consult = ConsultTemplate.objects.get(id=1)
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

    else:
        user_id = -1
        logout=False
        username = ''
        first_name = ''
        last_name = ''
        profile_image_path = ''

 
    return render(request, 'index-0.html',{'logout':logout,
                                           'user_id':user_id,
                                           'first':first_name,
                                           'last':last_name,
                                           'slides':slides,
                                           'consult':consult,
                                           'faqs':faqs,
                                           'qualifying':qquestions,
                                           'posts':posts,
                                           'milestones':milestones,
                                           'advantage_links':advantage_links,
                                           'profile_image':profile_image_path})


@csrf_exempt
def blogs(request, blog_id):
    consult = ConsultTemplate.objects.get(id=1)
    milestones = MileStone.objects.all()
    advantage_links = AdvantageLink.objects.filter(advantage_id=1)
    slides = Slide.objects.all()
    faqs = FAQ.objects.all()

    qquestions = QualifyQuestion.objects.all()

    try:
        posts = Post.objects.filter(id=int(blog_id))
    except Exception as e:
        posts = Post.objects.all()

    if request.user.is_authenticated():
        logout=True
        try:
           user_id = request.user.id
           username = request.user.username
           first_name = request.user.first_name
           last_name = request.user.last_name
           profile_image_path = ''
        except Exception, R:
           user_id = -1
           username = ''
           first_name = ''
           last_name = ''
           profile_image_path = ''

    else:
        user_id = -1
        logout=False
        username = ''
        first_name = ''
        last_name = ''
        profile_image_path = ''

    return render(request, 'index-0.html',{'logout':logout,
                                           'user_id':user_id,
                                           'first':first_name,
                                           'last':last_name,
                                           'service':'blog',
                                           'slides':slides,
                                           'consult':consult,
                                           'faqs':faqs,
                                           'qualifying':qquestions,
                                           'posts': posts,
                                           'milestones':milestones,
                                           'advantage_links':advantage_links,
                                           'profile_image':profile_image_path})


@csrf_exempt
def blog(request):
    consult = ConsultTemplate.objects.get(id=1)
    milestones = MileStone.objects.all()
    advantage_links = AdvantageLink.objects.filter(advantage_id=1)
    slides = Slide.objects.all()
    faqs = FAQ.objects.all()
    posts = Post.objects.all()
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

    else:
        user_id = -1
        logout=False
        username = ''
        first_name = ''
        last_name = ''
        profile_image_path = ''

    return render(request, 'index-0.html',{'logout':logout,
                                           'user_id':user_id,
                                           'first':first_name,
                                           'last':last_name,
                                           'service':'blog',
                                           'slides':slides,
                                           'faqs':faqs,
                                           'consult': consult,
                                           'qualifying':qquestions,
                                           'posts':posts,
                                           'milestones':milestones,
                                           'advantage_links':advantage_links,
                                           'profile_image':profile_image_path})




@csrf_exempt
def about(request):
    consult = ConsultTemplate.objects.get(id=1)
    milestones = MileStone.objects.all()
    advantage_links = AdvantageLink.objects.filter(advantage_id=1)
    slides = Slide.objects.all()
    faqs = FAQ.objects.all()
    posts = Post.objects.all()
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

    else:
        user_id = -1
        logout=False
        username = ''
        first_name = ''
        last_name = ''
        profile_image_path = ''

    return render(request, 'index-0.html',{'logout':logout,
                                           'user_id':user_id,
                                           'first':first_name,
                                           'last':last_name,
                                           'consult': consult,
                                           'service':'about',
                                           'slides':slides,
                                           'faqs':faqs,
                                           'qualifying':qquestions,
                                           'posts':posts,
                                           'milestones':milestones,
                                           'advantage_links':advantage_links,
                                           'profile_image':profile_image_path})


@csrf_exempt
def allservices(request):
    consult = ConsultTemplate.objects.get(id=1)
    milestones = MileStone.objects.all()
    advantage_links = AdvantageLink.objects.filter(advantage_id=1)
    slides = Slide.objects.all()
    faqs = FAQ.objects.all()
    posts = Post.objects.all()
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

    else:
        user_id = -1
        logout=False
        username = ''
        first_name = ''
        last_name = ''
        profile_image_path = ''

    return render(request, 'index-0.html',{'logout':logout,
                                           'user_id':user_id,
                                           'first':first_name,
                                           'last':last_name,
                                           'consult': consult,
                                           'service':'services',
                                           'slides':slides,
                                           'faqs':faqs,
                                           'qualifying':qquestions,
                                           'posts':posts,
                                           'milestones':milestones,
                                           'advantage_links':advantage_links,
                                           'profile_image':profile_image_path})


@csrf_exempt
def services(request, service):
    consult = ConsultTemplate.objects.get(id=1)
    milestones = MileStone.objects.all()
    advantage_links = AdvantageLink.objects.filter(advantage_id=1)
    slides = Slide.objects.all()
    faqs = FAQ.objects.all()
    posts = Post.objects.all()
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

    else:
        user_id = -1
        logout=False
        username = ''
        first_name = ''
        last_name = ''
        profile_image_path = ''

    return render(request, 'index-0.html',{'logout':logout,
                                           'user_id':user_id,
                                           'first':first_name,
                                           'last':last_name,
                                           'service':service,
                                           'slides':slides,
                                           'faqs':faqs,
                                           'consulut': consult,
                                           'qualifying':qquestions,
                                           'posts':posts,
                                           'milestones':milestones,
                                           'advantage_links':advantage_links,
                                           'profile_image':profile_image_path})

@csrf_exempt
def posts(request,page):
    consult = ConsultTemplate.objects.get(id=1)
    milestones = MileStone.objects.all()
    advantage_links = AdvantageLink.objects.filter(advantage_id=1)
    slides = Slide.objects.all()
    faqs = FAQ.objects.all()
    posts = Post.objects.all()
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

    else:
        user_id = -1
        logout=False
        username = ''
        first_name = ''
        last_name = ''
        profile_image_path = ''

    return render(request, 'index-0.html',{'logout':logout,
                                           'user_id':user_id,
                                           'first':first_name,
                                           'last':last_name,
                                           'consult': consult,
                                           'service':"blog",
                                           'slides':slides,
                                           'faqs':faqs,
                                           'qualifying':qquestions,
                                           'posts':posts,
                                           'milestones':milestones,
                                           'advantage_links':advantage_links,
                                           'profile_image':profile_image_path})


@csrf_exempt
def post(request):
    consult = ConsultTemplate.objects.get(id=1)
    milestones = MileStone.objects.all()
    advantage_links = AdvantageLink.objects.filter(advantage_id=1)
    slides = Slide.objects.all()
    faqs = FAQ.objects.all()
    posts = Post.objects.all()
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

    else:
        user_id = -1
        logout=False
        username = ''
        first_name = ''
        last_name = ''
        profile_image_path = ''

    return render(request, 'index-0.html',{'logout':logout,
                                           'user_id':user_id,
                                           'first':first_name,
                                           'last':last_name,
                                           'consult': consult,
                                           'service':"blog",
                                           'slides':slides,
                                           'faqs':faqs,
                                           'qualifying':qquestions,   
                                           'posts':posts,
                                           'milestones':milestones,
                                           'advantage_links':advantage_links,
                                           'profile_image':profile_image_path})


@csrf_exempt
def pricing(request):
    consult = ConsultTemplate.objects.get(id=1)
    if request.user.is_authenticated():
        logout=True
        try:
           user_id = request.user.id
           profile = User.objects.get(id=request.user.id)
           username = request.user.username
           first_name = request.user.first_name
           last_name = request.user.last_name
           profile_image_path = profile.profile_image_path
        except Exception, R:
           log = Logger(log='WE GOT SOME ERROR'+str(R))
           log.save()
           user_id = -1
           username = ''
           first_name = ''
           last_name = ''
           profile_image_path = ''

    else:
        user_id = -1
        logout=False
        username = ''
        first_name = ''
        last_name = ''
        profile_image_path = ''

    return render(request, 'index-3.html',{'logout':logout,
                                           'user_id':user_id,
                                           'consult': consult,
                                           'first':first_name,
                                           'last':last_name,
                                           'profile_image':profile_image_path})

@csrf_exempt
def ask(request):
    consult = ConsultTemplate.objects.get(id=1)
    if request.user.is_authenticated():
        logout=True
        try:
           user_id = request.user.id
           profile = User.objects.get(id=request.user.id)
           username = request.user.username
           first_name = request.user.first_name
           last_name = request.user.last_name
           profile_image_path = profile.profile_image_path
        except Exception, R:
           user_id = -1
           username = ''
           first_name = ''
           last_name = ''
           profile_image_path = ''

    else:
        user_id = -1
        logout=False
        username = ''
        first_name = ''
        last_name = ''
        profile_image_path = ''

    return render(request, 'index-3.html',{'logout':logout,
                                           'user_id':user_id,
                                           'first':first_name,
                                           'last':last_name,
                                           'consult': consult,
                                           'profile_image':profile_image_path})

@csrf_exempt
def contacts(request):
    consult = ConsultTemplate.objects.get(id=1)
    if request.user.is_authenticated():
        logout=True
        try:
           user_id = request.user.id
           profile = User.objects.get(id=request.user.id)
           username = request.user.username
           first_name = request.user.first_name
           last_name = request.user.last_name
           profile_image_path = profile.profile_image_path
 
        except Exception, R:
           user_id = -1
           username = ''
           first_name = ''
           last_name = ''
           profile_image_path = ''

    else:
        user_id = -1
        logout=False
        username = ''
        first_name = ''
        last_name = ''
        profile_image_path = ''

    return render(request, 'index-4.html',{'logout':logout,
                                           'user_id':user_id,
                                           'consult': consult,
                                           'first':first_name,
                                           'last':last_name,
                                           'profile_image':profile_image_path})

@csrf_exempt
def payment(request):
    consult = ConsultTemplate.objects.get(id=1)
    milestones = MileStone.objects.all()
    advantage_links = AdvantageLink.objects.filter(advantage_id=1)
    slides = Slide.objects.all()
    faqs = FAQ.objects.all()
    posts = Post.objects.all()
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

    else:
        user_id = -1
        logout=False
        username = ''
        first_name = ''
        last_name = ''
        profile_image_path = ''

    return render(request, 'index-0.html',{'logout':logout,
                                           'user_id':user_id,
                                           'first':first_name,
                                           'last':last_name,
                                           'service':'payment',
                                           'slides':slides,
                                           'consult': consult,
                                           'faqs':faqs,
                                           'posts':posts,
                                           'qualifying':qquestions, 
                                           'milestones':milestones,
                                           'advantage_links':advantage_links,
                                           'profile_image':profile_image_path})


@csrf_exempt
def toast(request):
    consult = ConsultTemplate.objects.get(id=1)
    if request.user.is_authenticated():
        logout=True
        try:
           user_id = request.user.id
           profile = User.objects.get(id=request.user.id)
           username = request.user.username
           first_name = request.user.first_name
           last_name = request.user.last_name
           profile_image_path = profile.profile_image_path
        except Exception, R:
           log = Logger(log='WE GOT SOME ERROR'+str(R))
           log.save()
           user_id = -1
           username = ''
           first_name = ''
           last_name = ''
           profile_image_path = ''

    else:
        user_id = -1
        logout=False
        username = ''
        first_name = ''
        last_name = ''
        profile_image_path = ''

    return render(request, 'toast.html',{'logout':logout,
                                           'first':first_name,
                                           'user_id':user_id,
                                           'consult': consult,
                                           'last':last_name,
                                           'profile_image':profile_image_path})


@csrf_exempt
def blog(request):
    if request.user.is_authenticated():
        logout=True
    else:
        logout=False

    return render(request, 'blog.html',{'blog':'blog.html'})

@csrf_exempt
def divorce(request):
    if request.user.is_authenticated():
        logout=True
        try: 
           user_id = request.user.id
           username = request.user.username
           first_name = request.user.first_name
           last_name = request.user.last_name
           profile_image_path = profile.profile_image_path
        except Exception, R:

           user_id = -1
           username = ''
           first_name = ''
           last_name = ''
           profile_image_path = ''

    else:
        logout=False
        username = ''
        first_name = ''
        last_name = ''
        profile_image_path = ''

    return render(request, 'divorce.html',{'divorce':'divorce.html','logout':logout,
                                                                    'user_id':user_id,
                                                                    'first':first_name,
                                                                    'last':last_name,
                                                                    'profile_image':profile_image_path})

@csrf_exempt
def logout(request):
    log_out(request)
    milestones = MileStone.objects.all()
    advantage_links = AdvantageLink.objects.filter(advantage_id=1)
    slides = Slide.objects.all()

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

    else:
        user_id = -1
        logout=False
        username = ''
        first_name = ''
        last_name = ''
        profile_image_path = ''

    return HttpResponseRedirect('/')


@csrf_exempt
def check_qualify(request):
    consult = ConsultTemplate.objects.get(id=1)
    milestones = MileStone.objects.all()
    advantage_links = AdvantageLink.objects.filter(advantage_id=1)
    slides = Slide.objects.all()
    faqs = FAQ.objects.all()
    posts = Post.objects.all()
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
           user_id = -1
           username = ''
           first_name = ''
           last_name = ''
           profile_image_path = ''

    else:
        user_id = -1
        logout=False
        username = ''
        first_name = ''
        last_name = ''
        profile_image_path = ''

    return render(request, 'index-0.html',{'logout':logout,
                                           'user_id':user_id,
                                           'first':first_name,
                                           'last':last_name,
                                           'service':'qualify',
                                           'slides':slides,
                                           'faqs':faqs,
                                           'qualifying':qquestions,
                                           'posts':posts,
                                           'consult': consult,
                                           'milestones':milestones,
                                           'advantage_links':advantage_links,
                                           'profile_image':profile_image_path})


@csrf_exempt
def contact(request):
    consult = ConsultTemplate.objects.get(id=1)
    milestones = MileStone.objects.all()
    advantage_links = AdvantageLink.objects.filter(advantage_id=1)
    slides = Slide.objects.all()
    faqs = FAQ.objects.all()
    posts = Post.objects.all()
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

    else:
        user_id = -1
        logout=False
        username = ''
        first_name = ''
        last_name = ''
        profile_image_path = ''

    return render(request, 'index-0.html',{'logout':logout,
                                           'user_id':user_id,
                                           'first':first_name,
                                           'last':last_name,
                                           'qualifying':qquestions,
                                           'service':'contact',
                                           'slides':slides,
                                           'faqs':faqs,
                                           'posts':posts,
                                           'consult': consult,
                                           'milestones':milestones,
                                           'advantage_links':advantage_links,
                                           'profile_image':profile_image_path})

@csrf_exempt
def pricing(request):
    consult = ConsultTemplate.objects.get(id=1)
    milestones = MileStone.objects.all()
    advantage_links = AdvantageLink.objects.filter(advantage_id=1)
    slides = Slide.objects.all()
    faqs = FAQ.objects.all()
    posts = Post.objects.all()
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

    else:
        user_id = -1
        logout=False
        username = ''
        first_name = ''
        last_name = ''
        profile_image_path = ''

    return render(request, 'index-0.html',{'logout':logout,
                                           'user_id':user_id,
                                           'first':first_name,
                                           'last':last_name,
                                           'consult': consult,
                                           'qualifying':qquestions,
                                           'service':'pricing',
                                           'slides':slides,
                                           'faqs':faqs,
                                           'posts':posts,
                                           'milestones':milestones,
                                           'advantage_links':advantage_links,
                                           'profile_image':profile_image_path})


@csrf_exempt
def faq(request):
    consult = ConsultTemplate.objects.get(id=1)
    milestones = MileStone.objects.all()
    advantage_links = AdvantageLink.objects.filter(advantage_id=1)
    slides = Slide.objects.all()
    faqs = FAQ.objects.all()
    posts = Post.objects.all()
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

    else:
        user_id = -1
        logout=False
        username = ''
        first_name = ''
        last_name = ''
        profile_image_path = ''

    return render(request, 'index-0.html',{'logout':logout,
                                           'user_id':user_id,
                                           'first':first_name,
                                           'last':last_name,
                                           'qualifying':qquestions,
                                           'service':'faq',
                                           'posts':posts,
                                           'consult': consult,
                                           'milestones':milestones,
                                           'advantage_links':advantage_links,
                                           'profile_image':profile_image_path})


class DashboardLogoutViewMixin(object):
    def get_context_data(self,**kwargs):
        context = super(DashboardLogoutViewMixin,
                  self).get_context_data(**kwargs)
        return context


class DashboardLogoutView(DashboardLogoutViewMixin, TemplateView):
    template_name = "inedex-0.html"
     
    @csrf_exempt
    def get(self, request):
        threshold=180
        if request.user.is_authenticated():
               logout(request)
        return render(request, 'index-0.html',{ 'FB_APP_ID' : settings.SOCIAL_AUTH_FACEBOOK_KEY,'logout':False })


user_resend_activation.connect(resend_activation_handler)
message_sent.connect(message_sent_handler)
 
