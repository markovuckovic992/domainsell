from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
import hashlib, random, requests, traceback
from datetime import datetime, timedelta
from mails.models import Offer, BlackList
from django.core import serializers
import json
import whois

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        return HttpResponseRedirect("/maintenance/")
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
    date = datetime.now().date() - timedelta(days=20)
    Offer.objects.filter(date__lt=date).delete()    
    main_status()
    serialized_obj = serializers.serialize('json', BlackList.objects.all())
    return HttpResponse(serialized_obj, content_type="application/json")

def main_status():
    offers = Offer.objects.filter(date__isnull=False, status=0)
    for offer in offers:
        uslov = True
        i = 0
        status = None
        while uslov:
            try:
                tube = whois.whois(offer.lead)
                status = tube['status']
                break
            except:
                print traceback.format_exc()
                if i > 5:
                    uslov = False
                else:
                    i += 1
        if status and 'pendingDelete' in status:
            Offer.objects.filter(id=data.id).update(status=1, updated=tube['updated_date'][0].date())
