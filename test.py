from django.core import mail
from django.conf import settings
import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'domainsell.settings'
django.setup()

connection = mail.get_connection()
connection.open()
emails = []
email = mail.EmailMultiAlternatives(
    'TEST',
    'TEST',
    'Web Domain Expert <' + settings.EMAIL_HOST_USER + '>',
    [offer.remail, offer.email],
    reply_to=("support@webdomainexpert.com", ),
)
emails.append(email)
connection.send_messages(emails)
connection.close()
