from urlparse import urlparse
from django.template import Library, Node, NodeList, TemplateSyntaxError
from django.utils.encoding import smart_str
from custom.metaprop.models import MetaProp, ContactMetaProp
from tagging.models import Tag, TaggedItem
from django import template
from django.template.defaultfilters import stringfilter


kw_paster = template.Library()
kw_pat = re.compile(r'^(?P<key>[\w]+)=(?P<value>.+)$')
register = Library()

"""
 Get the logo meta
"""
@register.simple_tag
def dashboard_meta(key, *args, **kwargs):
    pass

