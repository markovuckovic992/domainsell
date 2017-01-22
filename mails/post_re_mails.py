from django.template.loader import get_template
from django.template import Context, Template
from django.conf import settings
import codecs

### post offer
def po_msg1(domain_name, name, year, price):
    domain_name = domain_name.upper()

    subject = domain_name + ' - Get The Premium Domain Today. Ready for free traffic?'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/po1.html', 'r')
    content = file.read()
    htmly = Template(content)
    d = {
        "items": {
            'domain_name': domain_name,
            'name': name,
            'year': year,
            'price': price,
        }
    }

    html_content = htmly.render(Context(d))
    return [subject, html_content]

def po_msg2(domain_name, name, year, price):
    domain_name = domain_name.upper()

    subject = domain_name + ' - Increase daily traffic by 81% with this premium name'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/po2.html', 'r')
    content = file.read()
    htmly = Template(content)
    d = {
        "items": {
            'domain_name': domain_name,
            'name': name,
            'year': year,
            'price': price,
        }
    }

    html_content = htmly.render(Context(d))
    return [subject, html_content]


def po_msg3(domain_name, name, year, price):
    domain_name = domain_name.upper()

    subject = domain_name + ' - Have questions regarding domain acquisition? Let\'s set up a meeting'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/po3.html', 'r')
    content = file.read()
    htmly = Template(content)
    d = {
        "items": {
            'domain_name': domain_name,
            'name': name,
            'year': year,
            'price': price,
        }
    }

    html_content = htmly.render(Context(d))
    return [subject, html_content]


def po_msg4(domain_name, name, year, price):
    domain_name = domain_name.upper()

    subject = domain_name + ' - Did you forget something?'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/po4.html', 'r')
    content = file.read()
    htmly = Template(content)
    d = {
        "items": {
            'domain_name': domain_name,
            'name': name,
            'year': year,
            'price': price,
        }
    }

    html_content = htmly.render(Context(d))
    return [subject, html_content]


def po_msg5(domain_name, name, year, price):
    domain_name = domain_name.upper()

    subject = name + ', We want you to cut a Sweet Deal'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/po5.html', 'r')
    content = file.read()
    htmly = Template(content)
    d = {
        "items": {
            'domain_name': domain_name,
            'name': name,
            'year': year,
            'price': price,
        }
    }

    html_content = htmly.render(Context(d))
    return [subject, html_content]
### post release
def form_a_msg1(domain_name, name):
    domain_name = domain_name.upper()

    subject = domain_name + ' - Get The Premium Domain Today. Ready for free traffic?'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/pr1.html', 'r')
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

def form_a_msg2(domain_name, name):
    domain_name = domain_name.upper()

    subject = domain_name + ' - Increase daily traffic by 81% with this premium name'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/pr2.html', 'r')
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


def form_a_msg3(domain_name, name):
    domain_name = domain_name.upper()

    subject = domain_name + ' - Have questions regarding domain acquisition? Let\'s set up a meeting'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/pr3.html', 'r')
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


def form_a_msg4(domain_name, name):
    domain_name = domain_name.upper()

    subject = domain_name + ' - Did you forget something?'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/pr4.html', 'r')
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


def form_a_msg5(domain_name, name):
    domain_name = domain_name.upper()

    subject = name + ', We want you to cut a Sweet Deal'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/pr5.html', 'r')
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

def form_a_msg6(domain_name, name):
    domain_name = domain_name.upper()

    subject = 'Been busy? Your traffic generator ' + domain_name + ' is in your shopping cart'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/pr6.html', 'r')
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


def form_a_msg7(domain_name, name):
    domain_name = domain_name.upper()

    subject = 'I do not want your competitor to get ' + domain_name
    file = codecs.open(settings.EMAIL_TEMPLATES + '/pr7.html', 'r')
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


def form_a_msg8(domain_name, name):
    domain_name = domain_name.upper()

    subject = 'Can we talk about possible acquisition of alvarezinternational.com'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/pr8.html', 'r')
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


def form_a_msg9(domain_name, name):
    domain_name = domain_name.upper()

    subject = 'Close your file? Or are you still interested in acquiring ' + domain_name
    file = codecs.open(settings.EMAIL_TEMPLATES + '/pr9.html', 'r')
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


def form_a_msg10(domain_name, name):
    domain_name = domain_name.upper()

    subject = 'Your file closes in 10 days.'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/pr10.html', 'r')
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


def form_a_msg11(domain_name, name):
    domain_name = domain_name.upper()

    subject = 'Your file closes in 8 days. ' + domain_name + ' will no longer be available after that'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/pr11.html', 'r')
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


def form_a_msg12(domain_name, name):
    domain_name = domain_name.upper()

    subject = 'Your file closes in 6 days. ' + domain_name + ' will no longer be available after that'
    file = codecs.open(settings.EMAIL_TEMPLATES + '/pr12.html', 'r')
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