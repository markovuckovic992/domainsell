from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse, render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import hashlib, random, requests
from datetime import datetime
from mails.models import Offer, BlackList

@ensure_csrf_cookie
def receive_mails(request):
    try:
        hash_base_id = request.GET['id']
        entry = Offer.objects.get(hash_base_id=hash_base_id)
    except:
        return render_to_response('404.html', {})
    if entry.email:
        return render_to_response('offer_farewell.html', {'offer_id': entry.offer_id, 'again': 1})
    elif entry.offer_id:
        return render_to_response('offer_made.html', {'offer_id': entry.offer_id, 'again': 1})
    else:
        return render_to_response('offer.html', {'drop': entry.drop, 'base_id': entry.base_id, 'hash': hash_base_id})

def process_offer(request):
    base_id = request.POST['base_id']
    amount = request.POST['amount']
    offer_id = random.randint(1000000, 9999999)
    date = datetime.now().date()
    Offer.objects.filter(base_id=base_id).update(amount=amount, offer_id=offer_id, date=date)
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
    lead = Offer.objects.get(hash_base_id=hash_base_id).lead
    entry = BlackList.objects.filter(lead=lead)
    if not entry.exists():
        lead = Offer.objects.get(hash_base_id=hash_base_id).lead
        new = BlackList(lead=lead)
        new.save()
    Offer.objects.filter(hash_base_id=hash_base_id).delete()
    return render(request, 'unsubscribe.html', {})

@csrf_exempt
def addoffer(request):
    base_id = request.POST['base_id']
    lead = request.POST['lead']
    drop = request.POST['drop']
    hash_base_id = request.POST['hash_base_id']
    offer = Offer(base_id=base_id, lead=lead, drop=drop, hash_base_id=hash_base_id)
    offer.save()
    return HttpResponse('{"status": "success"}', content_type="application/json")

