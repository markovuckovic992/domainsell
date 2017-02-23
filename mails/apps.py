from django.template.loader import get_template
from django.template import Context, Template
from django.conf import settings
import codecs


def form_a_msg(domain_name, name):
    try:
        name = name.split()[0]
    except:
        name = ''

    domain_name = domain_name.upper()
    subject = 'Thank you for showing interest in ' + domain_name + '. Your free report is ready'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/po1.html', 'r')
    content = file.read()
    htmly = Template(content)
    d = {
        "items": {
            'domain_name': domain_name,
            'name': name,
        }
    }

    html_content = htmly.render(Context(d))
    return [subject, html_content]
