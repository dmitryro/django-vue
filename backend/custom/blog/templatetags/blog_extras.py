import logging
import re
from lxml import html, etree

import sys
from urlparse import urlparse
from django.template import Library, Node, NodeList, TemplateSyntaxError
from django.utils.encoding import smart_str
from django import template
from django.template.defaultfilters import stringfilter
import urllib2 as urllib
from cStringIO import StringIO
from django.contrib.auth.models import User
from custom.blog.models import Post
from custom.blog.models import Category
from custom.blog.models import Comment


register = template.Library()

kw_pat = re.compile(r'^(?P<key>[\w]+)=(?P<value>.+)$')
logger = logging.getLogger('sorl.thumbnail')

register = Library()

css_cleanup_regex = re.compile('((font|padding|margin)(-[^:]+)?|line-height):\s*[^;]+;')

"""
 Get the service provided  info data
"""
@register.simple_tag
def last_posted(a, b,  *args, **kwargs):

    try:
        try:
            posts = Post.obects.all().sort_by('-time-published')
            return posts
        except Exception, R:
            return ""

        if (b==1):
            return category.id

        elif (b==2):
            return category.name

        elif (b==3):
            return category.code


    except TypeError:
        print "Invalid argument type"

    except NameError:
        print "No result for this id"

