# For support@webdomainexpert.com - Alex says you can use Google SMTP details and it'll work

# So can you try that? p/w is - asdQWE123

# domainexpert , pw sbb12345

# import sendgrid
# from sendgrid import SendGridClient
# sg = SendGridClient('domainexpert', 'sbb12345', secure=True)

# message = sendgrid.Mail()
# message.add_to('Mister Mail <markovuckovic992@yahoo.com>')
# message.set_from('Mrs Mail <edomainexpert@gmail.com>')
# message.set_subject('Example')
# message.set_html('HTML Body')
# message.set_text('Text Body')
# msg = sg.send(message)


# from sendgrid import *

# sg = SendGridClient("f9_blKFgQoiWtQJ5FOmGwg")
# message = Mail()

# message.add_to("markovuckovic992@yahoo.com")
# message.set_from("edomainexpert@gmail.com")
# message.set_subject("Sending with SendGrid is Fun")
# message.set_html("and easy to do anywhere, even with Python")
# sg.send(message)
from django.conf import settings
import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'DomainScript.settings'
django.setup()

from django.core.mail import get_connection, send_mail
connection = get_connection(host='smtp.sendgrid.net', 
                            port=587, 
                            username='domainexpert', 
                            password='sbb12345', 
                            use_tls=True) 

send_mail('diditwork?', 'test message', 'edomainexpert@gmail.com', ['markovuckovic992@yahoo.com'], connection=connection)
