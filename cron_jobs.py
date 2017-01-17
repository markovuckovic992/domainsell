#!/usr/bin/python2.7
import django
import sys, traceback
import os
from django.core import mail
os.environ['DJANGO_SETTINGS_MODULE'] = 'domainsell.settings'
django.setup()

from mails.models import Offer
from django.conf import settings
from maintenance.lib import *

class CronJobs:
    def __init__(self):
        pass

    def send(self):
        offers = Offer.objects.filter(amount__isnull=False)[0:15]
        connection = mail.get_connection()
        connection.open()
        emails = []

        for offer in offers:
            if offer.phase == 1:
                to_send = sequnce_1(offer.stage, offer.last_email_date)
                if to_send:
                    sub, msg = eval(to_send + '(' + offer.drop + ', ' + offer.name + ')')
            elif offer.phase == 2:
                to_send = sequnce_2(offer.stage, offer.last_email_date)
                if to_send:
                    sub, msg = eval(to_send + '(' + offer.drop + ', ' + offer.name + ')')
            elif offer.phase == 3:
                to_send = sequnce_3(offer.stage, offer.last_email_date)
                if to_send:
                    sub, msg = eval(to_send + '(' + offer.drop + ', ' + offer.name + ')')
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
                Offer.objects.filter(id=offer.id).update(stage=stage)

        connection.send_messages(emails)
        connection.close()

c_j = CronJobs()
if len(sys.argv) > 1:
    if sys.argv[1] == 'send':
        c_j.send()
