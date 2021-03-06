from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse, render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.core.mail import send_mail
from django.core import mail
from django.conf import settings
import hashlib, random, requests, traceback
from datetime import datetime
from geoip import geolite2
from mails.models import Offer, BlackList
from mails.apps import *
from django.utils import timezone
import json
from os import popen

@ensure_csrf_cookie
def receive_mails(request):
    try:
        hash_base_id = request.GET['id']
        entry = Offer.objects.get(hash_base_id=hash_base_id)
    except:
        print traceback.format_exc()
        return render_to_response('_404.html', {})
    return render_to_response('index.html', {'drop': entry.drop, 'base_id': entry.base_id, 'hash': hash_base_id})

@ensure_csrf_cookie
def sales_page(request):
    try:
        hash_base_id = request.GET['id']
        entry = Offer.objects.get(hash_base_id=hash_base_id)
    except:
        print traceback.format_exc()
        return render_to_response('_404.html', {})
    return render_to_response('sales.html', {'drop': entry.drop, 'base_id': entry.base_id, 'hash': hash_base_id, 'amount':entry.amount})

@ensure_csrf_cookie
def sales_page_test(request):
    try:
        hash_base_id = request.GET['id']
        entry = Offer.objects.get(hash_base_id=hash_base_id)
    except:
        print traceback.format_exc()
        return render_to_response('_404.html', {})
    return render_to_response('sales_test.html', {'drop': entry.drop, 'base_id': entry.base_id, 'hash': hash_base_id, 'amount':entry.amount})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def process_offer(request):
    hash_ = request.POST['hash']
    amount = request.POST['amount']
    name = request.POST['name'].lower().capitalize()
    email = request.POST['email']
    contact = request.POST['contact']
    ip = get_client_ip(request)
    popen('python send.py ' + hash_ + ' "' +  amount + '" "' + name + '" "' + email + '" "' + contact + '" "' + unicode(ip) + '"')
    # t = threading.Thread(target=send_emails, args=[hash_, amount, name, email, contact, request.POST['ip']])
    # t.setDaemon(True)
    # t.start()
    # print '---------0----------'
    return HttpResponse('{"status": "success"}', content_type="application/json")

def process_offer_redirect(request):
    hash_base_id = request.GET['id']
    return render_to_response('offer_made.html', {'offer_id': Offer.objects.get(hash_base_id=hash_base_id).offer_id, 'hash': hash_base_id, 'again': 0})

def contact(request):
    email = request.POST['email_offer']
    contact = request.POST['phone_offer']
    hash_base_id = request.POST['hash']
    Offer.objects.filter(hash_base_id=hash_base_id).update(contact=contact, email=email)
    return HttpResponse('{"status": "success"}', content_type="application/json")

def thank(request):
    return render(request, 'ty.html', {})

def farewell(request):
    hash_base_id = request.GET['id']
    return render_to_response('offer_farewell.html', {'offer_id': Offer.objects.get(hash_base_id=hash_base_id).offer_id, 'again': 0})

def unsubscribe(request):
    hash_base_id = request.GET['id']
    email = Offer.objects.get(hash_base_id=hash_base_id).remail
    entry = BlackList.objects.filter(email=email)
    if not entry.exists():
        lead = Offer.objects.get(hash_base_id=hash_base_id).lead
        new = BlackList(email=email)
        new.save()
    # Offer.objects.filter(hash_base_id=hash_base_id).delete()
    return render(request, 'unsubscribe.html', {})

@csrf_exempt
def addoffer(request):
    base_id = int(request.POST['base_id'])
    lead = request.POST['lead']
    drop = request.POST['drop']
    hash_base_id = request.POST['hash_base_id']
    remail = request.POST['remail']
    if Offer.objects.filter(hash_base_id=hash_base_id).exists():
        return HttpResponse(status=204)
    elif Offer.objects.filter(base_id=base_id, lead=lead, drop=drop, remail=remail).exists():
        return HttpResponse(status=203)
    else:
        offer = Offer(base_id=base_id, lead=lead, drop=drop, hash_base_id=hash_base_id, remail=remail)
        offer.save()
    return HttpResponse('{"status": "success"}', content_type="application/json")

@csrf_exempt
def hello(request):
    try:
        hash_base_id = request.GET['id']
        entry = Offer.objects.get(hash_base_id=hash_base_id)
    except:
        print traceback.format_exc()
        return HttpResponse(json.dumps({'greeting': 'hello'}), content_type="application/json")
    response = {'drop': entry.drop, 'base_id': entry.base_id, 'hash': hash_base_id, 'amount':entry.amount}
    return HttpResponse(json.dumps(response), content_type="application/json")


@csrf_exempt
def process_offer_r(request):
    hash_ = request.GET['hash']
    amount = request.GET['amount']
    name = request.GET['name'].lower().capitalize()
    email = request.GET['email']
    contact = request.GET['contact']

    match = geolite2.lookup(request.GET['ip'])
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
        fail_silently=False,
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

    return HttpResponse('{"status": "success"}', content_type="application/json")
