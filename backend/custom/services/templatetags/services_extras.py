from django import template
from django.template import Library, Node, NodeList, TemplateSyntaxError

from custom.services.models import Package
from custom.services.models import Service

register = template.Library()

register = Library()

"""
 Get the service meta
"""

@register.simple_tag
def services_meta(a, b, state, *args, **kwargs):

    try:
        try:
            if state:
                Service.objects.get(state_id=state)
            else:
                service = Service.objects.get(id=int(a))
        except Exception, R:
            print R

        if (b==1):
            return '' if service.title is None else service.title

        elif (b==2):
            return '' if service.fees is None else service.fees

        elif (b==3):
            return '' if service.price is None else service.price

        elif (b==4):
            return '' if service.avatar is None else service.avatar

    except TypeError:
        print "Invalid argument type"

    except NameError:
        print "No result for this id"


"""
 Get the service meta
"""

@register.simple_tag
def packages_meta(a, b,  *args, **kwargs):

    try:
        try:
            package = Package.objects.get(id=int(a))
        except Exception, R:
            print R

        if (b==1):
            return '' if package.title is None else package.title

        elif (b==2):
            return '' if package.fees is None else package.fees

        elif (b==3):
            return '' if package.price is None else package.price

        elif (b==4):
            return '' if package.description is None else package.description


    except TypeError:
        print "Invalid argument type"

    except NameError:
        print "No result for this id"

