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

@ensure_csrf_cookie
def receive_mails(request):
    try:
        hash_base_id = request.GET['id']
        entry = Offer.objects.get(hash_base_id=hash_base_id)
    except:
        print traceback.format_exc()
        return render_to_response('404.html', {})
    return render_to_response('index.html', {'drop': entry.drop, 'base_id': entry.base_id, 'hash': hash_base_id})

def process_offer(request):
    base_id = request.POST['base_id']
    amount = request.POST['amount']
    name = request.POST['name'].lower().capitalize()
    email = request.POST['email']
    contact = request.POST['contact']

    match = geolite2.lookup(request.POST['ip'])
    code = match.country
    offer_id = random.randint(1000000, 9999999)
    date = datetime.now().date()
    Offer.objects.filter(base_id=base_id).update(
        amount=amount,
        offer_id=offer_id,
        date=date,
        name=name,
        email=email,
        contact=contact,
        code=code,
    )
    msg = '''
        amount= ''' + str(amount) + ''',
        offer_id= ''' + str(offer_id) + ''',
        date=''' + str(date) + ''',
        name=''' + str(name) + ''',
        whois email=''' + str(Offer.objects.get(base_id=base_id).remail) + ''',
        email=''' + str(email) + ''',
        contact=''' + str(contact) + ''',
        code=''' + str(code) + ''',
    '''
    send_mail(
        "Domain offer",  # Title
        msg,  # Body
        'Report <' + settings.EMAIL_HOST_USER + '>',
        ['rongax@gmail.com'],
        fail_silently=False,
    )

    offer = Offer.objects.get(base_id=base_id)
    msg = form_a_msg(offer.drop, name)

    if offer.email != offer.remail:
        sender = [offer.remail, offer.email]
    else:
        sender = [offer.remail]

    connection = mail.get_connection()
    connection.open()
    emails = []

    email = mail.EmailMultiAlternatives(
        msg[0],  # Title
        '',  # Body
        'Web Domain Expert <' + settings.EMAIL_HOST_USER + '>',
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
    Offer.objects.filter(hash_base_id=hash_base_id).delete()
    return render(request, 'unsubscribe.html', {})

@csrf_exempt
def addoffer(request):
    base_id = request.POST['base_id']
    lead = request.POST['lead']
    drop = request.POST['drop']
    hash_base_id = request.POST['hash_base_id']
    remail = request.POST['remail']
    if not Offer.objects.filter(base_id=base_id, lead=lead, drop=drop, hash_base_id=hash_base_id, remail=remail).exists():
        offer = Offer(base_id=base_id, lead=lead, drop=drop, hash_base_id=hash_base_id, remail=remail)
        offer.save()
    return HttpResponse('{"status": "success"}', content_type="application/json")
