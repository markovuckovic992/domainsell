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

def process_offer(request):
    hash_ = request.POST['hash']
    amount = request.POST['amount']
    name = request.POST['name'].lower().capitalize()
    email = request.POST['email']
    contact = request.POST['contact']

    match = geolite2.lookup(request.POST['ip'])
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
    if not Offer.objects.filter(base_id=base_id, lead=lead, drop=drop, hash_base_id=hash_base_id, remail=remail).exists():
        offer = Offer(base_id=base_id, lead=lead, drop=drop, hash_base_id=hash_base_id, remail=remail)
        offer.save()
    return HttpResponse('{"status": "success"}', content_type="application/json")
