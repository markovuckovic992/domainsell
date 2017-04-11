import django
import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'domainsell.settings'
django.setup()
from django.core.mail import send_mail
from django.core import mail
from django.conf import settings
import random, traceback
from datetime import datetime
from geoip import geolite2
from mails.models import Offer
from mails.apps import *
from django.utils import timezone

def send_emails(hash_, amount, name, email, contact, ip):
    try:
        print hash_, amount, name, email, contact, ip
        match = geolite2.lookup(ip)
        code = match.country
        offer_id = random.randint(1000000, 9999999)
        date = datetime.now().date()
        Offer.objects.filter(hash_base_id=hash_).update(
            amount=amount,
            offer_id=offer_id,
            date=date,
            name=name,
            email=email,
            contact=contact,
            code=code,
            done=0,
            phase=1,
            stage=2,
            last_email_date=timezone.now()
        )

        offr = Offer.objects.get(hash_base_id=hash_)
        msg = '''
            lead= ''' + str(offr.lead) + '\n' + ''',
            drop= ''' + str(offr.drop) + '\n' + ''',
            amount= ''' + str(amount) + '\n' + ''',
            offer_id= ''' + str(offer_id) + '\n' + ''',
            date=''' + str(date) + '\n' + ''',
            name=''' + str(name) + '\n' + ''',
            whois email=''' + str(offr.remail) + '\n' + ''',
            email=''' + str(email) + '\n' + ''',
            contact=''' + str(contact) + '\n' + ''',
            code=''' + str(code) + '\n' + ''',
        '''
        send_mail(
            "Domain offer",  # Title
            msg,  # Body
            'Report <' + settings.EMAIL_HOST_USER + '>',
            ['support@webdomainexpert.com'],
            fail_silently=True,
        )

        offer = Offer.objects.get(hash_base_id=hash_)
        msg = form_a_msg(offer.drop, name)

        if offer.email != offer.remail:
            sender = [offer.remail, offer.email]
        else:
            sender = [offer.remail]

        connection = mail.get_connection(host='smtp.gmail.com',
                                              port=587,
                                              username='support@webdomainexpert.com',
                                              password='asdQWE123',
                                              use_tls=True)
        connection.open()
        emails = []

        email = mail.EmailMultiAlternatives(
            msg[0],  # Title
            '',  # Body
            'Web Domain Expert <support@webdomainexpert.com>',
            [offer.remail, offer.email],
            reply_to=("support@webdomainexpert.com", ),
        )
        email.attach_alternative(msg[1], "text/html")
        emails.append(email)
        connection.send_messages(emails)
        connection.close()
    except:
        print traceback.format_exc()


if __name__ == '__main__':
    send_emails(
        sys.argv[1],
        sys.argv[2],
        sys.argv[3],
        sys.argv[4],
        sys.argv[5],
        sys.argv[6]
    )
