#!/usr/bin/python2.7
import django
import sys, traceback
import os
from django.core import mail
os.environ['DJANGO_SETTINGS_MODULE'] = 'domainsell.settings'
django.setup()

from mails.models import Offer, Setting
from django.conf import settings
from maintenance.lib import *

class CronJobs:
    def __init__(self):
        pass

    def send(self):   
        last_id = Setting.objects.get(id=1).last_id    
        offers = Offer.objects.filter(amount__isnull=False, id__gt=last_id, done=0)[0:15]
        connection = mail.get_connection()
        connection.open()
        emails = []
        tmp = 0
        for offer in offers:
            name = offer.name.split()[0]
            Max = 1
            if offer.phase == 0:
                Max = 1
                to_send = sequnce_0(offer.stage, offer.last_email_date)
                if to_send:
                    link = ('http://www.webdomainexpert.pw/offer/?id=' + str(offer.hash_base_id))
                    unsubscribe = ('http://www.webdomainexpert.pw/unsubscribe/?id=' + str(offer.hash_base_id))
                    sub, msg = eval(to_send + '("' + offer.drop + '", "' + name + '", "' + unsubscribe  + '", "' + link + '")')
            elif offer.phase == 1:
                Max = 5
                to_send = sequnce_1(offer.stage, offer.last_email_date)
                if to_send:
                    sub, msg = eval(to_send + '("' + offer.drop + '", "' + name + '", "' + str(offer.date_started.year)  + '", "' + str(offer.amount) + '")')
            elif offer.phase == 2:
                Max = 12
                to_send = sequnce_2(offer.stage, offer.last_email_date)
                if to_send:
                    sub, msg = eval(to_send + '("' + offer.drop + '", "' + name + '")')
            elif offer.phase == 3:
                Max = 5
                to_send = sequnce_3(offer.stage, offer.last_email_date)
                if to_send:
                    sub, msg = eval(to_send + '("' + offer.drop + '", "' + name + '")')
            else:
                to_send = None

            if to_send:
                email = mail.EmailMultiAlternatives(
                    sub,
                    '',
                    'Web Domain Expert <' + settings.EMAIL_HOST_USER + '>',
                    [offer.remail, offer.email],
                    reply_to=("support@webdomainexpert.com", ),
                )
                email.attach_alternative(msg, "text/html")
                emails.append(email)
                stage = offer.stage + 1
                done = 1 if Max < stage else 0
                Offer.objects.filter(id=offer.id).update(stage=stage, last_email_date=datetime.now().date(), done=done)
            tmp = offer.id
        connection.send_messages(emails)
        connection.close()
        Setting.objects.filter(id=1).update(last_id=tmp)


c_j = CronJobs()
if len(sys.argv) > 1:
    if sys.argv[1] == 'send':
        c_j.send()
