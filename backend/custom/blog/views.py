# Django Imports
import sys
import django.contrib.auth as auth
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q,Min,Max
from django.shortcuts import render
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.conf import settings

from rest_framework import filters
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework import generics


# Restless Endpoints 
from restless.views import Endpoint

from custom.utils.models import Logger

from models import Category
from models import Post
from models import Comment
from custom.users.models import Profile
from serializers import CategorySerializer
from serializers import PostSerializer
from serializers import CommentSerializer

import logging
logger = logging.getLogger(__name__)

@api_view(['POST', 'GET'])
@renderer_classes((JSONRenderer,))
@permission_classes([AllowAny,])
def publish_view(request):
    return Response({'message':'success'})    

class PostViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing post instances.
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing post instances.
    """
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


############################################
## Add comment to a post                  ##
## Extends: restless Endpoint             ##
## METHOD:  GET, POST                     ##
## Type:    Endpoint View (JSON)          ##
############################################

class GetCommentsView(Endpoint):

    @csrf_exempt
    def get(self, request):
        user = request.user
        post_id = request.params.get('post_id','')

        try:
            post = Post.objects.get(id=int(post_id))
            comments = Comment.objects.filter(post=post)
            serializer = CommentSerializer(comments,many=True)
            return {"comments":serializer.data}

        except Exception,R:
            logger.error('Internal Server Error: %s', request.path,
                exc_info=sys.exc_info(),
                extra={
                    'status_code': 500,
                    'request': request
                }
            )

            return {'message':'error','error':str(R)}

    @csrf_exempt
    def post(self, request):
        user = request.user
        post_id = request.data['post_id']

        try:
            post = Post.objects.get(id=int(post_id))
            comments = Comment.objects.filter(post=post)
            serializer = CommentSerializer(comments,many=True)
            return {"comments":serializer.data}

        except Exception,R:
            logger.error('Internal Server Error: %s', request.path,
                exc_info=sys.exc_info(),
                extra={
                    'status_code': 500,
                    'request': request
                }
            )

            return {'message':'error','error':str(R)}


class SaveCommentView(Endpoint):

    @csrf_exempt
    def post(self, request):
        post_id =  request.data['post_id']
        comment_id = request.data['comment_id']
        body = request.data['body']
          
        comment = Comment.objects.get(id=int(comment_id))
        comment.body = body
        comment.save()

        comments = Comment.objects.filter(post_id=int(post_id))
        serializer = CommentSerializer(comments,many=True)
            
        return {"comments":serializer.data}

    @csrf_exempt
    def get(self, request):
        post_id =  request.params.get('post_id','')
        comment_id = request.params.get('comment_id','')
        body = request.params.get('body','')

        comment = Comment.objects.get(id=int(comment_id))
        comment.body = body
        comment.save()

        comments = Comment.objects.filter(post_id=int(post_id))
        serializer = CommentSerializer(comments,many=True)

        return {"comments":serializer.data}


        
############################################
## Add comment to a post                  ##
## Extends: restless Endpoint             ##
## METHOD:  GET, POST                     ##
## Type:    Endpoint View (JSON)          ##
############################################

class AddCommentView(Endpoint):

    @csrf_exempt
    def get(self, request):
        user = request.user
        post_id = request.params.get('post_id','')
        body = request.params.get('body','')

        try:
            try:
               post = Post.objects.get(id=int(post_id))
               post.total_comments=post.total_comments+1
               post.save()
            except Exception,R:
               return {'message':'error','error':str(R)}
            anonymous_avatar = 'http://divorcesus.com/static/images/user_no_avatar.png'

            if not user.is_authenticated():

                 comment = Comment.objects.create(title='',
                                                  body=body,
                                                  username='Anonymous',
                                                  is_anonymous=True,
                                                  post=post,
                                                  avatar=anonymous_avatar,
                                                  is_flagged=False)
            else:

                 profile = Profile.objects.get(id=user.id)

                 comment = Comment.objects.create(title='',
                                                  body=body,
                                                  author=user,
                                                  username=user.username,
                                                  is_anonymous=False,
                                                  post=post,
                                                  avatar=profile.profile_image_path,
                                                  is_flagged=False)

            comments = Comment.objects.filter(post_id=int(post_id))
            serializer = CommentSerializer(comments,many=True)
            return {"comments":serializer.data}

        except Exception, R:
            return {'message':'error','error':str(R)}
   


    @csrf_exempt
    def post(self, request):
        user = request.user
        post_id = request.data['post_id']
        body = request.data['body']

        try:
            try:
               post = Post.objects.get(id=int(post_id))
               post.total_comments=post.total_comments+1
               post.save()
            except Exception,R:
               return {'message':'error','error':str(R)}

            if not user.is_authenticated():

                 comment = Comment.objects.create(title='',
                                                  body=body,
                                                  username='Anonymous',
                                                  is_anonymous=True,
                                                  post=post,
                                                  avatar=anonymous_avatar,
                                                  is_flagged=False)
            else:

                 profile = Profile.objects.get(id=user.id)

                 comment = Comment.objects.create(title='',
                                                  body=body,
                                                  author=user,
                                                  username=user.username,
                                                  is_anonymous=False,
                                                  post=post,
                                                  avatar=profile.profile_image_path,
                                                  is_flagged=False)


            comments = Comment.objects.filter(post_id=int(post_id))
            serializer = CommentSerializer(comments,many=True)
            return {"comments":serializer.data}

        except Exception, R:
            return {'message':'error','error':str(R)}
                  
 
############################################
## Add comment to a post                  ##
## Extends: restless Endpoint             ##
## METHOD:  GET, POST                     ##
## Type:    Endpoint View (JSON)          ##
############################################

class DeleteCommentView(Endpoint):

    @csrf_exempt
    def get(self, request):

        user = request.user
        comment_id = request.params.get('comment_id','')
        post_id = request.params.get('post_id','')

        try:
            comment = Comment.objects.get(id=int(comment_id))
            comment.delete()

            comments = Comment.objects.filter(post_id=int(post_id))
            serializer = CommentSerializer(comments,many=True)
            return {"comments":serializer.data}

        except Exception, R:
            return {'message':'error','error':str(R)}
 

    @csrf_exempt
    def post(self, request):
        comment_id = request.data['comment_id']
        post_id = request.data['post_id']

        try:
            comment = Comment.objects.get(id=int(comment_id))
            comment.delete()

            comments = Comment.objects.filter(post_id=int(post_id))
            serializer = CommentSerializer(comments,many=True)
            return {"comments":serializer.data}

        except Exception, R:
            return {'message':'error','error':str(R)}

############################################
## Add comment to a post                  ##
## Extends: restless Endpoint             ##
## METHOD:  GET, POST                     ##
## Type:    Endpoint View (JSON)          ##
############################################

class EditCommentView(Endpoint):

    @csrf_exempt
    def get(self, request):
        user = request.user


    @csrf_exempt
    def post(self, request):
        user = request.user



############################################
## Add a New Post view                    ##
## Extends: restless Endpoint             ##
## METHOD:  GET, POST                     ##
## Type:    Endpoint View (JSON)          ##
############################################

class AddPostView(Endpoint):

    @csrf_exempt
    def get(self, request):

        user = request.user
        title = request.params.get("title","")
        body = request.params.get("body","")  
        category_id = request.params.get("category_id","")

        try:

            category = Category.objects.get(id=int(category_id))
            post = Post.objects.create(title=title,body=body,
                                       category=category,author=user)
            posts = Post.objects.filter(author=user)
            serializer = PostSerializer(posts,many=True)
            return serializer.data

        except Exception,R:
            return {'message':'error '+str(R)}


    @csrf_exempt
    def post(self, request):

        user = request.user
        title = request.data["title"]
        body = request.data["body"]
        category_id = request.data["category_id"]
        link = request.data["link"]
 
        try:

            category = Category.objects.get(id=int(category_id))
            post = Post.objects.create(title=title,body=body,category=category,
                                       author=user,link=link,is_published=True)
            posts = Post.objects.filter(author=user)
            serializer = PostSerializer(posts,many=True)
            return serializer.data

        except Exception,R:
            log = Logger(log=str(R))
            log.save()
            return {'message':'error  '+str(R)}     


############################################
## Add a New Post view                    ##
## Extends: restless Endpoint             ##
## METHOD:  GET, POST                     ##
## Type:    Endpoint View (JSON)          ##
############################################

class SavePostView(Endpoint):

    @csrf_exempt
    def get(self, request):

        user = request.user
        post_id = request.params.get("post_id","")
        title = request.params.get("title","")
        body = request.params.get("body","")
        category_id = request.params.get("category_id","")
        link = request.params.get("link","")

        try:

            category = Category.objects.get(id=int(category_id))
            post = Post.objects.get(id=int(post_id))
            post.category=category
            post.title=title
            post.body=body
            post.link=link
            post.save()   
            posts = Post.objects.filter(author=user)
            serializer = PostSerializer(posts,many=True)
            return serializer.data

        except Exception,R:
            return {'message':'error '+str(R)}


    @csrf_exempt
    def post(self, request):
       
        user = request.user
        post_id = request.data["post_id"]
        title = request.data["title"]
        body = request.data["body"]
        category_id = request.data["category_id"]
        link = request.data["link"]

        try:

            category = Category.objects.get(id=int(category_id))
            post = Post.objects.get(id=int(post_id))
            post.category=category
            post.title=title
            post.body=body
            post.link=link
            post.save()
            posts = Post.objects.filter(author=user)
            serializer = PostSerializer(posts,many=True)
            return serializer.data

        except Exception,R:
            log = Logger(log=str(R))
            log.save()
            return {'message':'error  '+str(R)}


############################################
## Add a New Post view                    ##
## Extends: restless Endpoint             ##
## METHOD:  GET, POST                     ##
## Type:    Endpoint View (JSON)          ##
############################################

class GetAllPostsView(Endpoint):

    @csrf_exempt
    def get(self, request):

        user = request.user

        try:

            posts = Post.objects.all().order_by('-time_published')
      
            for post in posts:
               comments = Comment.objects.filter(post=post)
               post.total_comments = len(comments)
               post.save()
      
            serializer = PostSerializer(posts,many=True)
            return serializer.data

        except Exception,R:
            return {'message':'error '+str(R)}


    @csrf_exempt
    def post(self, request):

        user = request.user

        try:

            posts = Post.objects.all().order_by('-time_published')

            for post in posts:
               comments = Comment.objects.filter(post=post)
               post.total_comments = len(comments)
               post.save()

            serializer = PostSerializer(posts,many=True)
            return serializer.data

        except Exception,R:
            log = Logger(log=str(R))
            log.save()
            return {'message':'error  '+str(R)}




############################################
## Add a New Post view                    ##
## Extends: restless Endpoint             ##
## METHOD:  GET, POST                     ##
## Type:    Endpoint View (JSON)          ##
############################################

class GetPostsView(Endpoint):

    @csrf_exempt
    def get(self, request):

        user = request.user

        try:

            posts = Post.objects.filter(author=user)
            serializer = PostSerializer(posts,many=True)
            return serializer.data

        except Exception,R:
            return {'message':'error '+str(R)}


    @csrf_exempt
    def post(self, request):

        user = request.user

        try:

            posts = Post.objects.filter(author=user)
            serializer = PostSerializer(posts,many=True)
            return serializer.data

        except Exception,R:
            log = Logger(log=str(R))
            log.save()
            return {'message':'error  '+str(R)}


############################################
## Delete a Post view                     ##
## Extends: restless Endpoint             ##
## METHOD:  GET, POST                     ##
## Type:    Endpoint View (JSON)          ##
############################################

class DeletePostView(Endpoint):

    @csrf_exempt
    def get(self, request):
        user = request.user
        post_id = request.params.get("post_id","")

        try:
            post = Post.objects.get(id=int(post_id))
            post.delete()
            posts = Post.objects.filter(author=user)
            serializer = PostSerializer(posts,many=True)
            return serializer.data

        except Exception,R:
            log = Logger(log=str(R))
            log.save()
            return {'message':'error  '+str(R)}

        

    @csrf_exempt
    def post(self, request):
        user = request.user
        post_id = request.data["post_id"]


        try:
            post = Post.objects.get(id=int(post_id))
            post.delete()
            posts = Post.objects.filter(author=user)
            serializer = PostSerializer(posts,many=True)
            return serializer.data

        except Exception,R:
            log = Logger(log=str(R))
            log.save()
            return {'message':'error  '+str(R)}


############################################
## Archive a Post view                    ##
## Extends: restless Endpoint             ##
## METHOD:  GET, POST                     ##
## Type:    Endpoint View (JSON)          ##
############################################

class ArchivePostView(Endpoint):

    @csrf_exempt
    def get(self, request):

        user = request.user
        post_id = request.params.get("post_id","")

    @csrf_exempt
    def post(self, request):

        user = request.user
        post_id = request.data["post_id"]


############################################
## Delete a Post view                     ##
## Extends: restless Endpoint             ##
## METHOD:  GET, POST                     ##
## Type:    Endpoint View (JSON)          ##
############################################

class ReadPostView(Endpoint):

    @csrf_exempt
    def get(self, request):
        user = request.user
        post_id = request.params.get("post_id","")

        try:
            post = Post.objects.get(id=int(post_id))
            serializer = PostSerializer(post,many=False)
            return serializer.data

        except Exception,R:
            log = Logger(log=str(R))
            log.save()
            logger.error('Internal Server Error: %s', request.path,
                exc_info=sys.exc_info(),
                extra={
                    'status_code': 500,
                    'request': request
                }
            )

            return {'message':'error  '+str(R)}



    @csrf_exempt
    def post(self, request):
        user = request.user
        post_id = request.data["post_id"]


        try:
            post = Post.objects.get(id=int(post_id))
            serializer = PostSerializer(post,many=False)
            return serializer.data

        except Exception,R:
            log = Logger(log=str(R))
            log.save()
            logger.error('Internal Server Error: %s', request.path,
                exc_info=sys.exc_info(),
                extra={
                    'status_code': 500,
                    'request': request
                }
            )

            return {'message':'error  '+str(R)}

