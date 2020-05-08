# This is where our intelligence shines
# Pipeline is where we manage user accounts

import urllib2
import json
import logging
from simplejson import loads
import urllib
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
import django.contrib.auth as auth
from django.shortcuts import redirect
from social_core.pipeline.partial import partial
from django.contrib.auth import logout
from django.conf import settings
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import default_storage as storage
from django.core.files.base import ContentFile
from django.db.models import Min, Max
from social.apps.django_app.views import _do_login
from social.backends.facebook import FacebookOAuth2
from requests import request, HTTPError
from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify
from django_facebook.utils import get_user_model, mass_get_or_create, \
    cleanup_oauth_url, get_profile_model, parse_signed_request, hash_key, \
    try_get_profile, get_user_attribute

import logging

from StringIO import StringIO
from PIL import Image
import urllib2
import random
import json
import os
import re
import sys

from custom.users.models import Profile
from custom.utils.models import Logger
from signals import facebook_strategy_used
from signals import googleplus_strategy_used
from signals import twitter_strategy_used
from signals import linkedin_strategy_used

from callbacks import twitter_profile_handler
from callbacks import facebook_profile_handler
from callbacks import googleplus_profile_handler
from callbacks import linkedin_profile_handler

@partial
def check_username(backend, details, user, response, is_new=False,*args,**kwargs):
         try:
              min_id = User.objects.filter(email=user.email).aggregate(id=Min('id'))
              usr_id=int(min_id['id'])
              is_new=False
              usr = User.objects.get(id=usr_id)
              if usr.id < user.id:
                   return {'user':usr}
              else:
                  return {'user':user} 

         except ObjectDoesNotExist:
              min_id = User.objects.filter(username=user.username).aggregate(id=Min('id'))
              usr_id=int(min_id['id'])
              is_new=False
              usr = User.objects.get(id=usr_id)
              if usr.id < user.id:
                  return {'user':usr}

              else:
                  user.username = str(user.id)
                  user.save()
                  return {'user':user}

         except Exception,R:
              if user:
                 return {'user':user}


@partial
def fix_twitter_linkedin(backend, details, uid, user=None, *args, **kwargs):
    #return {'user': user}

    if backend.name == 'twitter':
        social = backend.strategy.storage.user.get_social_auth('twitter', uid)
        try:
            profile = Profile.objects.get(twitter_uid=uid)
            profile.is_linkedin_signup_used = True
            profile.save()
            is_new = False
        except ObjectDoesNotExist as e:
            is_new = True
            profile = Profile.objects.create(id=user.id,
                                             username=user.username,
                                             is_new=True,
                                             email=user.email,
                                             first_name=user.first_name,
                                             last_name=user.last_name,
                                             twitter_uid=uid,
                                             is_twitter_signup_used=True,
                                             user=user)
            
        twitter_strategy_used.send(sender=profile.user,
                                   instance=profile.user,
                                   email=profile.email,
                                   profile_picture=None,
                                   is_new=is_new,
                                   kwargs=None)

        return {'user': profile.user}
#    elif backend.name == 'facebook':
#        email = details['email']
#        log = Logger(log="WE USE FACEBOOK {}".format(email))
#        log.save()
        
#        return {'user': user}

    elif backend.name == 'linkedin-oauth2' or  backend.name == 'facebook':
        email = details['email']

        try:
            max_id = User.objects.filter(email=email).aggregate(id=Max('id'))

            max_usr_id=int(max_id['id'])

            min_id = User.objects.filter(email=email).aggregate(id=Min('id'))
            min_usr_id=int(min_id['id'])

            if min_usr_id < max_usr_id:
                u = User.objects.get(id=max_usr_id)
                u.delete()

            usr =  User.objects.get(id=min_usr_id)
            is_new = False
            user = usr
        except ObjectDoesNotExist as e:
            is_new = True
            profile = Profile.objects.create(id=user.id,
                                             username=user.username,
                                             is_new=True,
                                             email=email,
                                             first_name=user.first_name,
                                             last_name=user.last_name,
                                             twitter_uid=uid,
                                             is_linkedin_signup_used=True,
                                             user=user)

            avatar_url = response.get('pictureUrls', {}).get('values', [None])[0]

            if not avatar_url:
                avatar_url = response.get('pictureUrl')

            log = Logger("LINKED AVATAR {}".format(avatar_url))
            log.save()

            profile.profile_image_path=avatar_url
            profile.save()

        linkedin_strategy_used.send(sender=user, 
                                    instance = user,
                                    new_id=user.id,
                                    is_new=is_new,
                                    email=email,
                                    request=request,
                                    kwargs=None)

        return {'user': user}

    return {'user': user}

@partial
def check_duplicate(backend, details, user, response, is_new=False,*args,**kwargs):
         #if user:
          #   return {'user':user}

         if backend.name == 'facebook':
             email = details['email']
             try:
                  min_id = User.objects.filter(email=email).aggregate(id=Min('id'))
                  usr_id=int(min_id['id'])
                  is_new=False
                  usr = User.objects.get(id=usr_id)
                  return {"user":usr}
             except ObjectDoesNotExist:
                  return {"user":None}
             except Exception, R:
                  return {"user":None}

         if backend.name == 'google-oauth2':
             email = details['email']
             try:
                  min_id = User.objects.filter(email=email).aggregate(id=Min('id'))
                  usr_id=int(min_id['id'])
                  is_new=False
                  usr = User.objects.get(id=usr_id)
                  return {"user":usr}
             except ObjectDoesNotExist:
                  return {"user":None}
             except Exception, R:
                  return {"user":None}

         if backend.name == 'linkedin-oauth2':
             email = details['email']
             try:
                  min_id = User.objects.filter(email=email).aggregate(id=Min('id'))
                  usr_id=int(min_id['id'])
                  is_new=False
                  usr = User.objects.get(id=usr_id)
                  return {"user":usr}
             except ObjectDoesNotExist:
                  return {"user":None}
             except Exception, R:
                  return {"user":None}


@partial
def consolidate_profiles(backend, details, user, response, is_new=False,*args,**kwargs):
    if user.email:
        min_id = User.objects.filter(email=user.email).aggregate(id=Min('id'))
        usr_id=min_id['id']
        usr = User.objects.get(id=usr_id)
    else:
        usr = user

    if backend.name == 'linkedin-oauth2':
        skip_user = False

        image_small = response.get('pictureUrl', None)
        image_large = response.get('pictureUrls', {})



        try:
            try:
                 min_id = User.objects.filter(email=user.email).aggregate(id=Min('id'))
                 usr_id=int(min_id['id'])
                 is_new=False
                 usr = User.objects.get(id=usr_id)

            except ObjectDoesNotExist:
                 email = response.get('emailAddress')
                 min_id = User.objects.filter(email=email).aggregate(id=Min('id'))
                 usr_id=int(min_id['id'])
                 is_new=False
                 usr = User.objects.get(id=usr_id)
            except Exception,R:
                 usr = user

            if usr.id < user.id:
                is_new = False
                try:
                    user.profilesummary.delete()
                except Exception, R:
                    pass
                try:
                    user.profile.delete()
                except Exception, R:
                    pass
                try:
                    user.delete()
                except Exception, R:
                     pass

                return {'user':usr}
            else:
                is_new = True
                usr = user


        except ObjectDoesNotExist:
            usr = user
            skip_user = False

        try:
             profile=Profile.objects.get(id=usr.id)
        except ObjectDoesNotExist:
             profile = Profile.objects.create(id=usr.id,
                                              username=usr.username,
                                              is_new=True,
                                              email=usr.email,
                                              first_name=usr.first_name,
                                              last_name=usr.last_name,
                                              is_linkedin_signup_used=True,
                                              user=usr)

        if profile.is_user_avatar==False:
            avatar_url = response.get('pictureUrls', {}).get('values', [None])[0]
            if not avatar_url:
               avatar_url = response.get('pictureUrl')

            profile.profile_image_path=avatar_url
            profile.save()




    elif backend.name == 'twitter':
        profile_image_path = response.get('profile_image_url', '').replace('_normal', '')
        try:
            profile = Profile.objects.get(profile_image_path=profile_image_path)
            usr = profile.user
        except ObjectDoesNotExist:
            profile = Profile.objects.create(id=user.id,
                                             username=user.username,
                                             is_new=True,
                                             email=user.email,
                                             is_twitter_signup_used=True,
                                             first_name=user.first_name,
                                             last_name=user.last_name,
                                             user=user)
            is_new = True
            usr = user

        if profile.is_user_avatar==False:            

            avatar_url = response.get('profile_image_url', '').replace('_normal', '')
            profile.profile_image_path=avatar_url
            profile.is_twitter_avatar=True
            profile.save()
                
            if avatar_url:
                profile_picture = avatar_url
            else:
                profile_picture = settings.PROFILE_IMAGE_PATH
        else:
            profile_picture = profile.profile_image_path
            
        try:
            email = usr.email
            twitter_strategy_used.send(sender=usr, 
                                       instance=usr,
                                       is_new=is_new,
                                       email=email,
                                       profile_picture=profile_picture,
                                       kwargs=None)
        except Exception as e:
            log = Logger(log='SOMETHING WHENT WRONG IN TWITTER %s'%str(e))
            log.save()

        return {'user':usr}



    elif backend.name == 'google-oauth2':
        email = user.email
        log = Logger(log='WE ARE IN GOOGLE - user {} {} {}'.format(user.first_name, user.last_name, user.email))
        log.save()

        skip_user = False
        
        try:
            try:
                 min_id = User.objects.filter(email=user.email).aggregate(id=Min('id'))
                 usr_id=int(min_id['id'])
                 is_new=False
                 usr = User.objects.get(id=usr_id)
             
            except ObjectDoesNotExist:
                 min_id = User.objects.filter(username=user.username).aggregate(id=Min('id'))
                 usr_id=int(min_id['id'])
                 is_new=False
                 usr = User.objects.get(id=usr_id)
            except Exception,R:
                 usr = user

            if usr.id < user.id:
                is_new = False
                try:
                    user.profilesummary.delete()
                except Exception, R:
                    pass
                try:
                    user.profile.delete()
                except Exception, R:
                    pass
                try:
                    user.delete()
                except Exception, R:
                     pass

                return {'user':usr}
            else:
                is_new = True
                usr = user


        except ObjectDoesNotExist:
            usr = user
            skip_user = False
        except Exception, R:
            usr = user
            skip_user = False

        try:
             profile=Profile.objects.get(id=usr.id)
        except ObjectDoesNotExist:
             profile = Profile.objects.create(id=usr.id,
                                              username=usr.username,
                                              is_new=True,
                                              email=usr.email,
                                              first_name=usr.first_name,
                                              last_name=usr.last_name,
                                              is_google_signup_used=True,
                                              user=usr)



        if profile.is_user_avatar==False:
                 
                 try:
                     profile_picture_url=str(response['image'].get('url'))[:-2] # Read the original google avatar

                     profile_picture_url=profile_picture_url+'200' # provide the size
                 except Exception as e:
                     profile_picture_url = 'https://divorcesus.com/media/avatars/default.png' 

                 input_file = StringIO(urllib2.urlopen(profile_picture_url).read()) # read the file into buffer
                 image = Image.open(input_file)   # Create an image
                 output = StringIO()
                 format = 'PNG' # or 'JPEG' or whatever you want
                 image.save(output, format)   # Format image
                 contents = output.getvalue() # Get the size
                 size = len(contents) # The default avatar has size 4712 so we know we have to replace it


                 if size <= 5000: # Verify size and replace if smaller than 5000
                       profile_picture = settings.PROFILE_IMAGE_PATH
                       is_google_avatar = False
                 else:
                       profile_picture = profile_picture_url
                       is_google_avatar = True

                 output.close() # Close the buffer
                 profile.is_google_avatar=True 
                 profile.profile_image_path=profile_picture_url #Save the avatar in profile url
                 profile.save()
         
        if profile.is_new:
                 profile_picture_url=str(response['image'].get('url'))[:-2] # Read the original google avatar

                 profile_picture_url=profile_picture_url+'200' # provide the size

                 input_file = StringIO(urllib2.urlopen(profile_picture_url).read()) # read the file into buffer
                 image = Image.open(input_file)   # Create an image
                 output = StringIO()
                 format = 'PNG' # or 'JPEG' or whatever you want
                 image.save(output, format)   # Format image
                 contents = output.getvalue() # Get the size
                 size = len(contents) # The default avatar has size 4712 so we know we have to replace it


                 if size <= 5000: # Verify size and replace if smaller than 5000
                       profile_picture = settings.PROFILE_IMAGE_PATH
                       is_google_avatar = False
                 else:
                       profile_picture = profile_picture_url
                       is_google_avatar = True

                 if not profile_picture:
                    profile_picture = settings.PROFILE_IMAGE_PATH

                 profile.profile_image_path=profile_picture

                
                 usr.username = usr.username.lower()
                 profile.username = usr.username.lower()
                 profile.save()
                 profile.save()
        else:
            profile_picture =  profile.profile_image_path


        if profile.is_new:
                     is_new = True
        else:
                     is_new = False

        usr.email = email
        usr.save()

        googleplus_strategy_used.send(sender=usr, instance = usr,
                                            is_new=is_new, email=email,
                                            profile_picture=profile_picture, kwargs=None)
        return {'user': usr}



    elif backend.name == 'facebook':
        email = user.email
        log = Logger(log='WE ARE IN FACEBOOK - user {} {} {}'.format(user.first_name, user.last_name, user.email))
        log.save()

        skip_user = False

        try:

            try:
                 min_id = User.objects.filter(email=user.email).aggregate(id=Min('id'))
                 usr_id=int(min_id['id'])
                 is_new=False
                 usr = User.objects.get(id=usr_id)

            except ObjectDoesNotExist:
                 min_id = User.objects.filter(username=user.username).aggregate(id=Min('id'))
                 usr_id=int(min_id['id'])
                 is_new=False
                 usr = User.objects.get(id=usr_id)
            except Exception,R:
                 usr = user

            if usr.id < user.id:
                is_new = False
                try:
                    user.profile.delete()
                except Exception, R:
                    pass
                try:
                    user.profile.delete()
                except Exception, R:
                    pass
                try:
                    user.delete()
                except Exception, R:
                     pass

                return {'user':usr}
            else:
                usr = user

        except ObjectDoesNotExist:
            usr = user
            skip_user = False
        except Exception, R:
            usr = user
            skip_user = False

        try:
             profile=Profile.objects.get(id=usr.id)
        except ObjectDoesNotExist:
             is_new=True
             profile = Profile.objects.create(id=usr.id,
                                              username=usr.username,
                                              is_new=True,
                                              email=usr.email,
                                              first_name=usr.first_name,
                                              last_name=usr.last_name,
                                              is_facebook_signup_used=True,
                                              user=usr)



        if profile.is_user_avatar==False:
            if profile.is_google_avatar==False:
                 profile_picture_url= "http://graph.facebook.com/%s/picture?type=large"%response['id'] # Read the original google avatar


                 input_file = StringIO(urllib2.urlopen(profile_picture_url).read()) # read the file into buffer
                 image = Image.open(input_file)   # Create an image
                 output = StringIO()
                 format = 'PNG' # or 'JPEG' or whatever you want
                 image.save(output, format)   # Format image
                 contents = output.getvalue() # Get the size
                 size = len(contents) # The default avatar has size 4712 so we know we have to replace it


                 if size <= 6000: # Verify size and replace if smaller than 5000
                       profile_picture = settings.PROFILE_IMAGE_PATH
                       is_facebook_avatar = False
                 else:
                       profile_picture = profile_picture_url
                       is_facebook_avatar = True

                 output.close() # Close the buffer
                 profile.is_facebook_avatar=True
                 profile.profile_image_path=profile_picture_url #Save the avatar in profile url
                 profile.save()

                 
        if profile.is_new:
                     is_new = True
        else:
                     is_new = False


        usr.email = email
        usr.save()

        facebook_strategy_used.send(sender=usr, instance = usr,
                                          new_id=user.id,
                                          is_new=is_new,
                                          email=email,
                                          facebook_id=response['id'],
                                          request=request,
                                          kwargs=None)
        return {'user':usr}


linkedin_strategy_used.connect(linkedin_profile_handler)
twitter_strategy_used.connect(twitter_profile_handler)
googleplus_strategy_used.connect(googleplus_profile_handler)
facebook_strategy_used.connect(facebook_profile_handler)
