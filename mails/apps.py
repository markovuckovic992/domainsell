from __future__ import unicode_literals

from django.apps import AppConfig


class MailsConfig(AppConfig):
    name = 'mails'

def form_a_msg(domain_name, name):  
    domain_name = domain_name.upper() 
    line_offer = "<a href='" + str(link) + "'>OFFER PAGE LINK</a>"
    link_un = "<a href='" + unsubscribe + "'>[LINK]</a>"

    subject = 'Thank you for showing interest in ' + domain_name + '  Your free report is ready'
    msg =  'Hi, ' + name  
    msg += '<br/>'
    msg += 'Congratulations on making the right choice for your business. Thousands of entrepreneurs have successfully turned their businesses around using Web Domain Expert’s unique domain service. ' 
    msg += '<br/>' 
    msg += 'You get a lot more than just a premium domain. ' 
    msg += '<br/>' 
    msg += 'You will learn How To Double Your Traffic In Less Than A Month For FREE!'
    msg += '<br/>'
    msg += 'We’ve not only helped our clients get the best possible domains for their brands, but also showed them how to drive an enormous amount of traffic to their sites.' 
    msg += '<br/>' 
    msg += 'I have received your offer for the domain ' + domain_name + ' and together with my team will do our best to ensure you receive this valuable domain. ' 
    msg += '<br/>' 
    msg += 'I will be in touch with you regularly from now on to tell you more about traffic generation and the best SEO practices today, so you can take them onboard and increase revenue. ' 
    msg += '<br/>' 
    msg += 'If you have any question, please feel free to send me an email. I promise to get back to you as soon as I can. ' 
    msg += '<br/>'
    msg += '<br/>'
    msg += 'Best regards, '
    msg += 'Ronnie'
    msg += '<br/>'
    msg += '<br/>'
    msg += '<a href="http://webdomainexpert.com/">Web Domain Expert</a>'

    return [subject, msg]