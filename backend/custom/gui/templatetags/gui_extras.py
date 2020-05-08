import logging
import re
from lxml import html, etree
import sys
from cStringIO import StringIO
from urlparse import urlparse
import urllib2 as urllib
import html2text
from django.template import Library, Node, NodeList, TemplateSyntaxError
from django.utils.encoding import smart_str
from django import template
from django.template.defaultfilters import stringfilter
from django.contrib.auth.models import User
from custom.users.models import Profile
from custom.users.models import TeamMember
from custom.users.models import AboutUs
from custom.users.models import MileStone
from custom.users.models import Advantage
from custom.users.models import AdvantageLink
from custom.gui.models import Logo
from custom.users.models import Testimonial
from custom.gui.models import ContactInfo
from custom.gui.models import Service
from custom.gui.models import Article
from custom.gui.models import AskTemplate
from custom.gui.models import ConsultTemplate
from custom.gui.models import FrontBlock
from custom.services.models import Package
from custom.services.models import PackageTerm
from custom.messaging.models import Message
from custom.payments.models import CreditCard
from custom.payments.models import Address
from custom.blog.models import Post
from custom.blog.models import Comment
from custom.utils.models import Logger


h = html2text.HTML2Text()

register = template.Library()

kw_pat = re.compile(r'^(?P<key>[\w]+)=(?P<value>.+)$')
logger = logging.getLogger('sorl.thumbnail')

register = Library()

css_cleanup_regex = re.compile('((font|padding|margin)(-[^:]+)?|line-height):\s*[^;]+;')
def _cleanup_elements(elem):
    """
    Removes empty elements from HTML (i.e. those without text inside).
    If the tag has a 'style' attribute, we remove the css attributes we don't want.
    """
    if elem.text_content().strip() == '':
        elem.drop_tree()
    else:
        if elem.attrib.has_key('style'):
            elem.attrib['style'] = css_cleanup_regex.sub('', elem.attrib['style'])
        for sub in elem:
            _cleanup_elements(sub)

def cleanup_html(string):
    """
    Makes generated HTML (i.e. ouput from the WYSISYG) look almost decent.
    """
    try:
        elem = html.fromstring(string)
        _cleanup_elements(elem)
        html_string = html.tostring(elem)
        lines = []

        for line in html_string.splitlines():
            line = line.rstrip()
            if line != '': lines.append(line)

        return '\n'.join(lines)

    except etree.XMLSyntaxError:
        return string


"""
 Get the dashboard meta
"""
@register.simple_tag
def dashboard_meta(a, b,  *args, **kwargs):
    try:
       user = User.objects.get(id=int(a))
    except Exception as e:
       return 'invalid user'

    if b==1:
        try:
           messages = Message.objects.filter(receiver_id=user.id)
           return len(messages)
        except Exception as e:
           return 0

    elif b==2:
       try:
          messages = Message.objects.filter(sender_id=user.id)
          return len(messages)
       except Exception as e:
          return 0

    elif b==3:
       try:
          posts = Post.objects.filter(author_id=user.id)
          return len(posts)
       except Exception as e:
          return 0

    elif b==4:
       try:
          comments = Comment.objects.filter(author_id=user.id)
          return len(comments)
       except Exception as e:
          return 0

    elif b==5:
       try:
          messages = Message.objects.filter(receiver_id=user.id, is_seen=False)
          return len(messages)
       except Exception as e:
          return 0

    elif b==6:
       try:
          addresses = Address.objects.filter(user_id=user.id)
          return len(addresses)
       except Exception as e:
          return 0

    elif b==7:
        return 0

    elif b==8:
        return 0

    elif b==9:
        return 0


"""
 Get Front Page Block
"""
@register.simple_tag
def front_meta(a, b,  *args, **kwargs):

    try:
        block = FrontBlock.objects.get(id=int(a))

        if (b==1):
            return '' if block.title is None else h.handle(block.title)

        elif (b==2):
            return '' if block.body is None else h.handle(block.body)

        elif (b==3):

            return '' if block.link is None else h.handle(block.link)

    except TypeError:
        log = Logger(log="Failure to parse type")
        log.save()

    except NameError:
        log = Logger(log="Name error")
        log.save()


    except Exception as e:
        log = Logger(log="Failure to read record {}".format(e))
        log.save()


"""
 Get the logo meta
"""
@register.simple_tag
def user_meta(a, b,  *args, **kwargs):

    try:
        try:
            user = User.objects.get(id=int(a))
            profile = user.profile
        except Exception as R:
            print R

        if (b==1):
            return '' if user.first_name is None else user.first_name

        elif (b==2):
            return '' if user.last_name is None else user.last_name

        elif (b==3):
            
            if not  profile.profile_image_path or len(profile.profile_image_path)==0:
               return '/media/avatars/default.png'

            return profile.profile_image_path

        elif b==4:
            return user.email if profile.email else ""

        elif b==5:
           return profile.phone if profile.phone else ""
               

        elif b==6:
            return profile.username if profile.username else ""

 
 
    except TypeError:
        print "Invalid argument type"

    except NameError:
        print "No result for this id"


"""
 Get the logo meta
"""
@register.simple_tag
def aboutus_meta(a, b,  *args, **kwargs):

    try:
        try:
            aboutus = AboutUs.objects.get(id=int(a))
        except Exception, R:
            return ""

        if (b==1):
            return h.handle(aboutus.title)

        elif (b==2):
            return h.handle(aboutus.subtitle)

        elif (b==3):
            return h.handle(aboutus.body)

        elif (b==4):
            return aboutus.avatar

    except TypeError:
        print "Invalid argument type"

    except NameError:
        print "No result for this id"

"""
 Package term meta
"""
@register.simple_tag
def package_meta(a, *args, **kwargs):

    try:
        try:
            term = PackageTerm.objects.get(id=int(a))
        except Exception as r:
            return ""

        return h.handle(term.term)

    except TypeError:
        print "Invalid argument type"

    except NameError:
        print "No result for this id"


"""
 Get the article meta
"""
@register.simple_tag
def article_meta(a, b,  *args, **kwargs):

    try:
        try:
            article = Article.objects.get(id=int(a))
        except Exception as R:
            return ""

        if (b==1):
            return article.title

        elif (b==2):
            return h.handle(article.teaser)

        elif (b==3):
            return h.handle(article.body)



    except TypeError:
        print "Invalid argument type"

    except NameError:
        print "No result for this id"



"""
 Get the logo meta
"""
@register.simple_tag
def member_meta(a, b,  *args, **kwargs):

    try:
        try:
            member = TeamMember.objects.get(id=int(a))
        except Exception, R:
            return ""

        if (b==1):
            return h.handle(member.title)
        elif (b==2):
            return h.handle(member.bio)
        elif (b==3):
            return member.avatar

    except TypeError:
        print "Invalid argument type"

    except NameError:
        print "No result for this id"

"""
 Testimonial meta
"""
@register.simple_tag
def testimonial_meta(a, b,  *args, **kwargs):

    try:
        try:
            testimonial = Testimonial.objects.get(id=int(a))
        except Exception as ex:
            return ""

        if (b==1):
            return h.handle(testimonial.name)
        elif (b==2):
            return h.handle(testimonial.body)
        elif (b==3):
            return "https://divorcesus.com/media/{}".format(testimonial.avatar)

    except TypeError:
        print "Invalid argument type"

    except NameError:
        print "No result for this id"


"""
 Get the logo meta
"""
@register.simple_tag
def milestone_meta(a, b,  *args, **kwargs):

    try:
        try:
            milestone = MileStone.objects.get(id=int(a))
        except Exception, R:
            return ""

        if (b==1):
            return h.handle(milestone.title)
        elif (b==2):
            return h.handle(milestone.year)
        elif (b==3):
            return h.handle(milestone.body)

    except TypeError:
        print "Invalid argument type"

    except NameError:
        print "No result for this id"



"""
 Get the advantage data
"""
@register.simple_tag
def advantage_meta(a, b,  *args, **kwargs):

    try:
        try:
            advantage = Advantage.objects.get(id=int(a))
        except Exception, R:
            return ""

        if (b==1):
            return advantage.title
        elif (b==2):
            return h.handle(advantage.section_one)
        elif (b==3):
            return h.handle(advantage.section_two)
        elif (b==4):
            return h.handle(advantage.section_three)


    except TypeError:
        print "Invalid argument type"

    except NameError:
        print "No result for this id"




"""
 Get the logo  data
"""
@register.simple_tag
def logo_meta(a, b,  *args, **kwargs):

    try:
        try:
            logo = Logo.objects.get(id=int(a))
        except Exception, R:
            return ""

        if (b==1):
            return logo.logo
        elif (b==2):
            return logo.width
        elif (b==3):
            return logo.height
        elif (b==4):
            return logo.color


    except TypeError:
        print "Invalid argument type"

    except NameError:
        print "No result for this id"




"""
 Get the contact  info data
"""
@register.simple_tag
def contact_meta(a, b,  *args, **kwargs):

    try:
        try:
            contact = ContactInfo.objects.get(id=int(a))
        except Exception as R:
            return ""

        if (b==1):
            return h.handle(contact.statement)

        elif (b==2):
            return h.handle(contact.address1)

        elif (b==3):
            return h.handle(contact.address2)

        elif (b==4):
            return h.handle(contact.city)

        elif (b==5):
            return h.handle(contact.state)

        elif (b==6):
            return h.handle(contact.zipcode)

        elif (b==7):
            return h.handle(contact.tollfree)

        elif (b==8):
            return h.handle(contact.phone)

        elif (b==9):
            return h.handle(contact.fax)

        elif (b==10):
            return h.handle(contact.email)

        elif (b==0):
            return h.handle(contact.header)





    except TypeError:
        print "Invalid argument type"

    except NameError:
        print "No result for this id"

@register.simple_tag
def faq_meta(a,   *args, **kwargs):
    return  h.handle(unicode(a)) #html2text(q)



@register.simple_tag
def service_meta(a, b,  *args, **kwargs):
    """
     Get the service provided  info data
    """

    try:
        service = Service.objects.get(id=int(a))

        if (b==1):
            return service.title

        elif (b==2):
            return service.statement

        elif (b==3):
            return cleanup_html(service.description)

        elif (b==4):
            return service.service

    except TypeError:
        print "Invalid argument type"
        return ""

    except NameError:
        print "No result for this id"
        return ""

    except Exception as e:
        return ""


@register.simple_tag
def consult_meta(a, b,  *args, **kwargs):

    try:
        try:
            consult = ConsultTemplate.objects.get(id=int(a))
        except Exception as R:
            return ""

        if (b==1):
            return h.handle(cleanup_html(consult.consult_intro))

        elif (b==2):
            return  "<section>ONE</section><section>TWO<section>"

        elif (b==3):
            return h.handle(consult.disclaimer)



    except TypeError:
        print "Invalid argument type"

    except NameError:
        print "No result for this id"


@register.simple_tag
def ask_meta(a, b,  *args, **kwargs):

    try:
        try:
            ask = AskTemplate.objects.get(id=int(a))
        except Exception, R:
            return ""

        if (b==1):
            return h.handle(ask.ask_intro)

        elif (b==2):
            return ask.agreement

        elif (b==3):
            return h.handle(ask.disclaimer)



    except TypeError:
        print "Invalid argument type"

    except NameError:
        print "No result for this id"


@register.simple_tag
def billing_meta(a, b,  *args, **kwargs):

    try:
       user = User.objects.get(id=int(a))
    except Exception as e:
       return 'invalid user'

    try:
        try:
            address = Address.objects.get(user_id=user.id, is_default=True)
        except Exception, R:
            return ""

        if (b==1):
            return h.handle(address.address1)

        elif (b==2):
            return h.handle(address.address2)


        elif (b==3):
            return h.handle(address.city)

        elif (b==4):
            return address.state.id

        elif (b==5):
            return h.handle(address.country)
        
        elif (b==6):
            return h.handle(address.zip_or_postal)



    except TypeError:
        print "Invalid argument type"

    except NameError:
        print "No result for this id"

