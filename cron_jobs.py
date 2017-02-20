#!/usr/bin/python
import django
import sys, traceback
import os, pytz
from datetime import datetime, timedelta
from django.core import mail
from itertools import chain
os.environ['DJANGO_SETTINGS_MODULE'] = 'domainsell.settings'
django.setup()

from mails.models import Offer, Setting
from django.conf import settings
from maintenance.lib import *
from django.db.models import Q
from random import randint

hosts = [
    'webdomainexpert.us',
    'webdomainexpert.host',
    'webdomainexpert.site',
    'webdomainexpert.club',
]

class CronJobs:
    def __init__(self):
        pass

    def send(self):
        two_days_ago = (datetime.now() - timedelta(days=2))
        two_days_ago = pytz.timezone('Europe/Belgrade').localize(two_days_ago)

        last_id = Setting.objects.get(id=1).last_id

        offers = list(chain(Offer.objects.filter(
            Q(id__gt=last_id, done=0, phase__in=[1, 2, 3], stage__gt=1, last_email_date__lt=two_days_ago)
        )[0:2],Offer.objects.filter(
            Q(id__gt=last_id, done=0, phase=0, last_email_date__lt=two_days_ago)            
        )[0:6]))
        for offer in offers:
            print offer.phase

        # connection1 = mail.get_connection()
        # connection1.open()
        # connection2 = mail.get_connection(host='smtp.gmail.com',
        #                                   port=587,
        #                                   username='support@webdomainexpert.com',
        #                                   password='asdQWE123',
        #                                   use_tls=True)

        # emails1 = []
        # emails2 = []

        # tmp = 0
        # for offer in offers:
        #     try:
        #         name = offer.name.split()[0]
        #     except:
        #         name = ''
        #     Max = 1
        #     if offer.phase == 0:
        #         Max = 1
        #         to_send = sequnce_0(offer.stage, offer.last_email_date)
        #         iterator = randint(0, 3)
        #         host = str(hosts[iterator])
        #         if to_send:
        #             link = ('http://www.' + host + '/offer/?id=' + str(offer.hash_base_id))
        #             unsubscribe = ('http://www.' + host + '/unsubscribe/?id=' + str(offer.hash_base_id))
        #             sub, msg = eval(to_send + '("' + offer.drop + '", "' + name + '", "' + unsubscribe + '", "' + link + '")')
        #     elif offer.phase == 1:
        #         Max = 5
        #         to_send = sequnce_1(offer.stage, offer.last_email_date)
        #         if to_send:
        #             amount = "{0:.2f}".format(offer.amount)
        #             sub, msg = eval(to_send + '("' + offer.drop + '", "' + name + '")')
        #     elif offer.phase == 2:
        #         Max = 12
        #         to_send = sequnce_0(offer.stage, offer.last_email_date)
        #         iterator = randint(0, 3)
        #         host = str(hosts[iterator])
        #         to_send = sequnce_2(offer.stage, offer.last_email_date)
        #         if to_send:
        #             link = ('http://www.' + host + '/sales/?id=' + str(offer.hash_base_id))
        #             sub, msg = eval(to_send + '("' + offer.drop + '", "' + name + '", "' + link +'")')
        #     elif offer.phase == 3:
        #         Max = 5
        #         to_send = sequnce_3(offer.stage, offer.last_email_date)
        #         if to_send:
        #             sub, msg = eval(to_send + '("' + offer.drop + '", "' + name + '")')
        #     else:
        #         to_send = None

        #     if to_send:
        #         if offer.phase > 0:
        #             fr_email = 'support@webdomainexpert.com'
        #             bcc = "w.expert@yahoo.com"
        #         else:
        #             fr_email = settings.EMAIL_HOST_USER
        #             bcc = "bcc-webdomainexpert@outlook.com"

        #         email = mail.EmailMultiAlternatives(
        #             sub,
        #             '',
        #             'Web Domain Expert <' + fr_email + '>',
        #             [offer.remail, offer.email],
        #             reply_to=("support@webdomainexpert.com", ),
        #             bcc=[bcc],
        #         )
        #         email.attach_alternative(msg, "text/html")

        #         if offer.phase > 0:
        #             emails2.append(email)
        #         else:
        #             emails1.append(email)

        #         stage = offer.stage + 1
        #         done = 1 if Max < stage else 0
        #         Offer.objects.filter(id=offer.id).update(stage=stage, last_email_date=datetime.now(), done=done)
        #     tmp = offer.id
        # connection1.send_messages(emails1)
        # connection2.send_messages(emails2)
        # connection1.close()
        # connection2.close()
        # Setting.objects.filter(id=1).update(last_id=tmp)


c_j = CronJobs()
if len(sys.argv) > 1:
    if sys.argv[1] == 'send':
        c_j.send()
