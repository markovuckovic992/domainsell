from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse
from mails.models import Offer


def receive_mails(request):
    try:
        base_id = request.GET['base_id']
        entry = Offer.objects.get(base_id=base_id)
    except:
        return render_to_response('404.html', {})
    if entry.email:
        return render_to_response('offer_farewell.html', {'offer_id': entry.offer_id, 'again': 1})
    elif entry.offer_id:
        return render_to_response('offer_made.html', {'offer_id': entry.offer_id, 'again': 1})
    else:
        return render_to_response('offer.html', {'lead': entry.lead, 'base_id': base_id})

def process_offer(request):
    base_id = request.POST['base_id']
    amount = request.POST['amount']
    Offer.objects.filter(base_id=base_id).update(amount=amount)
    return render_to_response('offer_made.html', {'offer_id': Offer.objects.get(base_id=base_id).offer_id, 'again': 0})

def contact(request):
    email = request.POST['email']
    contact = request.POST['contact']
    base_id = request.POST['base_id']
    Offer.objects.filter(base_id=base_id).update(contact=contact, email=email)
    return render_to_response('offer_farewell.html', {'offer_id': Offer.objects.get(base_id=base_id).offer_id, 'again': 0})
