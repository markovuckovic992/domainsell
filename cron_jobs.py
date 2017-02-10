#!/usr/bin/python
import django
import sys, traceback
import os
from datetime import datetime, timedelta
from django.core import mail
os.environ['DJANGO_SETTINGS_MODULE'] = 'domainsell.settings'
django.setup()

from mails.models import Offer, Setting
from django.conf import settings
from maintenance.lib import *
from django.db.models import Q


class CronJobs:
    def __init__(self):
        pass

    def send(self):
        two_days_ago = (datetime.now() - timedelta(days=1)).date()
        last_id = Setting.objects.get(id=1).last_id
        offers = Offer.objects.filter(
            Q(id__gt=last_id, done=0, phase=0, last_email_date__lt=two_days_ago) |
            Q(id__gt=last_id, done=0, phase__in=[1, 2, 3])
        )[0:15]  # | Q(phase__in=[1, 2, 3], stage=1)
        connection1 = mail.get_connection()
        connection1.open()
        connection2 = mail.get_connection(host='smtp.sendgrid.net',
                                          port=587,
                                          username='domainexpert',
                                          password='sbb12345',
                                          use_tls=True)
        emails1 = []
        emails2 = []

        tmp = 0
        for offer in offers:
            try:
                name = offer.name.split()[0]
            except:
                name = ''
            Max = 1
            if offer.phase == 0:
                Max = 1
                to_send = sequnce_0(offer.stage, offer.last_email_date)
                if to_send:
                    link = ('http://www.webdomainexpert.pw/offer/?id=' + str(offer.hash_base_id))
                    unsubscribe = ('http://www.webdomainexpert.pw/unsubscribe/?id=' + str(offer.hash_base_id))
                    sub, msg = eval(to_send + '("' + offer.drop + '", "' + name + '", "' + unsubscribe + '", "' + link + '")')
            elif offer.phase == 1:
                Max = 5
                to_send = sequnce_1(offer.stage, offer.last_email_date)
                if to_send:
                    amount = "{0:.2f}".format(offer.amount)
                    sub, msg = eval(to_send + '("' + offer.drop + '", "' + name + '", "' + str(offer.date_started.year) + '", "' + str(amount) + '")')
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
                if offer.phase > 1:
                    to_email = 'edomainexpert@gmail.com'
                else:
                    to_email = settings.EMAIL_HOST_USER

                email = mail.EmailMultiAlternatives(
                    sub,
                    '',
                    'Web Domain Expert <' + to_email + '>',
                    [offer.remail, offer.email],
                    reply_to=("support@webdomainexpert.com", ),
                    bcc=["bcc-webdomainexpert@outlook.com"],
                )
                email.attach_alternative(msg, "text/html")

                if offer.phase > 1:
                    emails2.append(email)
                else:
                    emails1.append(email)

                stage = offer.stage + 1
                done = 1 if Max < stage else 0
                Offer.objects.filter(id=offer.id).update(stage=stage, last_email_date=datetime.now().date(), done=done)
            tmp = offer.id
        connection1.send_messages(emails1)
        connection2.send_messages(emails2)
        connection1.close()
        connection2.close()
        Setting.objects.filter(id=1).update(last_id=tmp)


c_j = CronJobs()
if len(sys.argv) > 1:
    if sys.argv[1] == 'send':
        c_j.send()
