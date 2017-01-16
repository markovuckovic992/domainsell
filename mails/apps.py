from __future__ import unicode_literals

from django.apps import AppConfig


class MailsConfig(AppConfig):
    name = 'mails'

def form_a_msg(domain_name, name):  
    domain_name = domain_name.upper() 
    subject = 'Thank you for showing interest in ' + domain_name + '  Your free report is ready'
    msg =  'Hi, ' + name  
    msg += '<br/>'
    msg += '<br/>'
    msg += 'Congratulations on making the right choice for your business. Thousands of entrepreneurs have <br/> successfully turned their businesses around using Web Domain Expert is unique domain service. ' 
    msg += '<br/><br/>' 
    msg += 'You get a lot more than just a premium domain. ' 
    msg += '<br/><br/>' 
    msg += 'You will learn How To Double Your Traffic In Less Than A Month For FREE!'
    msg += '<br/><br/>'
    msg += 'We have not only helped our clients get the best possible domains for their brands, but also <br/> showed them how to <u>drive an enormous amount of traffic</u> to their sites.' 
    msg += '<br/><br/>' 
    msg += 'I have received your offer for the domain ' + domain_name + ' and together with my team will do our best to ensure you receive this valuable domain. ' 
    msg += '<br/><br/>' 
    msg += 'I will be in touch with you regularly from now on to tell you more about traffic generation and <br/>the best SEO practices today, so you can take them onboard and increase revenue. ' 
    msg += '<br/>' 
    msg += 'If you have any question, please feel free to send me an email. I promise to get back to you as<br/> soon as I can. ' 
    msg += '<br/>'
    msg += '<br/><br/>'
    msg += 'Best regards, <br/>'
    msg += 'Ronnie'
    msg += '<br/>'
    msg += '<br/><br/>'
    msg += '<a href="http://webdomainexpert.com/">Web Domain Expert</a>'

    return [subject, msg]
