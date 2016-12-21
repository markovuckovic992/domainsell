from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse, render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout
import hashlib, random, requests, traceback
from datetime import datetime, timedelta
from mails.models import Offer, BlackList
from django.core import serializers
import json
import whois

@ensure_csrf_cookie
def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect("/maintenance/")
        else:
            return render(request, 'login.html')
    return render(request, 'login.html')

def homeLogout(request):
    logout(request)
    return HttpResponseRedirect("/home_login/")

@login_required
def monitoring(request):
    offers = Offer.objects.filter(date__isnull=False)
    return render_to_response('monitoring.html', {'offers': offers})

@login_required
def revert_state(request):
    offer_id = request.POST['id']
    control = request.POST['control']
    Offer.objects.filter(id=offer_id).update(sale=control)
    return HttpResponse('{"status": "success"}', content_type="application/json")

@csrf_exempt
def delete_old_data(request):
    offers = Offer.objects.filter(status=0)
    for offer in offers:
        data = whois.whois(offer.drop)        
        if 'pendingDelete' in str(data['status']):
            try:
                Offer.objects.filter(id=offer.id).update(status=1, updated=data['updated_date'][0])
            except:
                Offer.objects.filter(id=offer.id).update(status=1, updated=data['updated_date'])
    date = datetime.now().date() - timedelta(days=20)
    hashes = serializers.serialize('json', Offer.objects.filter(date_started__lt=date))
    Offer.objects.filter(date_started__lt=date).delete()
    serialized_obj = serializers.serialize('json', BlackList.objects.all())
    response = {
        'hashes': hashes,
        'blk': serialized_obj,
    }
    return HttpResponse(json.dumps(response), content_type="application/json")
