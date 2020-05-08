from django.contrib.auth.models import User
from django.dispatch import receiver
# Datetime related imports
from datetime import datetime
from datetime import date
from datetime import time
from datetime import tzinfo


from django.core.exceptions import ObjectDoesNotExist
# Email imports
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# smtp imports
import smtplib
import urllib2
from smtplib import SMTPRecipientsRefused
import string
import codecs
from StringIO import StringIO
import urllib2
import random
import json
import os
import re
# Custom Imports
from custom.metaprop.models import ProfileMetaProp


from custom.users.decorators import run_async
from custom.tasks.models import TaskLog
from custom.users.models import Profile
from custom.utils.models import Logger

from signals import payment_send_confirmation_email

@receiver(payment_send_confirmation_email,sender=User)
def payment_send_confirmation_email_handler(sender,**kwargs):
     contact = kwargs['contact']
     try:
        
        task = TaskLog.objects.get(user_id=contact.id,job='sending_payment_email')
     except Exception, R:
        task = TaskLog.objects.create(user_id=contact.id, job='sending_payment_email', is_complete=False)
        payment = kwargs['payment']


        process_payment_office_email(payment, contact)


def process_payment_office_email(payment, contact):
    try:
        timeNow = datetime.now()
        profile = ProfileMetaProp.objects.get(pk=1)
        FROM = 'Grinberg & Segal <{}>'.format(profile.from_email)
        USER = profile.user_name
        PASSWORD = profile.password
        PORT = profile.smtp_port
        SERVER = profile.smtp_server
        TO = contact.email
        email_cc_one = profile.to_email
        email_cc_two = profile.to_email_secondary
        email_cc_three = profile.to_email_third        

        log = Logger(log = 'We are sending email to {}'.format(payment))
        log.save()

        SUBJECT = 'Your payment has been processed'
        try:
            path = "templates/payment_message.html"

            f = codecs.open(path, 'r')
            m = f.read()
            mess = m
            mess = string.replace(m, '[fullname]', str(payment.fullname))
            mess = string.replace(mess,'[greeting]', 'Dear')
            mess = string.replace(mess,'[greeting_statement]','You just made an online payment for Grinberg and Segal Family Law Division.')
            line1 = "<p>Please give us 1 to 3 busintess days to follow up.</p>"
            line2 = "<p>Truly Yours,<br/>"
            line3 = "Grinberg and Segal Family Law Division</p>"

            mess = string.replace(mess,'[wait_statement]',"{}{}{}".format(line1, line2, line3))
            mess = string.replace(mess, '[greeting_global_link]', 'Gringerg and Segal Family Law Division')
            mess = string.replace(mess, '[global_link]', 'https://divorcesus.com')
            mess = string.replace(mess, '[greeting_locale]', 'New York, NY, USA')
            mess = string.replace(mess, '[invoice]', payment.payment.invoice)
            mess = string.replace(mess, '[address1]', str(payment.address1))
            mess = string.replace(mess, '[address2]', str(payment.address2))
            mess = string.replace(mess, '[city]', str(payment.city))
            mess = string.replace(mess, '[state]', str(payment.state))
            mess = string.replace(mess, '[zip]', str(payment.zipcode))
            mess = string.replace(mess, '[phone]', str(payment.phone))
            mess = string.replace(mess, '[email]', str(payment.email))
            mess = string.replace(mess, '[package_type]', str(payment.package_type))
            mess = string.replace(mess, '[package_price]', str(payment.package_price))

        #    mess = string.replace(mess,'[link]',link)

        except Exception as R:
            log = Logger(log="WE FAILED LOUDLY "+str(R))
            log.save()
        message = mess

         
        log =  Logger(log="WE are about to send ... ")
        log.save()

        MESSAGE = MIMEMultipart('alternative')
        MESSAGE['subject'] = SUBJECT
        MESSAGE['To'] = TO
        MESSAGE['Bcc'] = '{},{},{}'.format(email_cc_one, email_cc_two, email_cc_three)
        MESSAGE['From'] = FROM
        MESSAGE.preamble = """
                Your mail reader does not support the report format.
                Please visit us <a href="http://www.mysite.com">online</a>!"""

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
        HTML_BODY  = MIMEText(message, 'html','utf-8')
        MESSAGE.attach(HTML_BODY)
        msg = MESSAGE.as_string()
        server = smtplib.SMTP(SERVER+':'+PORT)
        server.ehlo()
        server.starttls()
        server.login(USER,PASSWORD)
        server.sendmail(FROM, TO, msg)
        server.quit()
        log = Logger(log="WE HAVE SENT EMAILS ")
        log.save()
    except SMTPRecipientsRefused:
        pass
    except ObjectDoesNotExist:
        pass
    except Exception, R:
        log = Logger(log="ANOTHER FAILURE HERE: "+str(R))
        log.save()




