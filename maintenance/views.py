from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse, render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout
import hashlib, random, requests, traceback
from datetime import datetime, timedelta
from mails.models import Offer, BlackList
from django.core import serializers
import json
from os import popen

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

@login_required
def check_status(request):
    offers = Offer.objects.filter(~Q(status=1), date__isnull=False)
    msg = ''
    for offer in offers:
        try:
            tube = popen("whois '" + str(offer.drop) + "' | egrep -i 'Status|Updated Date'", 'r')
            resp = tube.read()
            resp = resp.replace('Status:', '').replace('\n', '').replace('\r', '')
            tube.close()
            statuses = resp.split(' ')
            if 'pendingDelete' in str(statuses):
                Offer.objects.filter(id=offer.id).update(status=1, updated=datetime.now().date())
            else:
                Offer.objects.filter(id=offer.id).update(status=0)
        except:
            statuses = 'ERROR'
            msg += (traceback.format_exc() + '\n')
            Offer.objects.filter(id=offer.id).update(status=2)
        msg += ('DROP: ' + str(offer.drop) + str(statuses))
        msg += '\n --------------------- \n'
    return HttpResponse('{"status": ' + msg + '}', content_type="application/json")

@csrf_exempt
def delete_old_data(request):
    offers = Offer.objects.filter(~Q(status=1), date__isnull=False)
    for offer in offers:
        try:
            data = whois.whois(offer.drop)
            if 'pendingDelete' in str(data['status']):
                try:
                    Offer.objects.filter(id=offer.id).update(status=1, updated=data['updated_date'][0])
                except:
                    Offer.objects.filter(id=offer.id).update(status=1, updated=data['updated_date'])
        except:
            Offer.objects.filter(id=offer.id).update(status=2)
    date = datetime.now().date() - timedelta(days=20)
    hashes = serializers.serialize('json', Offer.objects.filter(date_started__lt=date, amount__isnull=True))
    Offer.objects.filter(date_started__lt=date, amount__isnull=True).delete()
    serialized_obj = serializers.serialize('json', BlackList.objects.all())
    response = {
        'hashes': hashes,
        'blk': serialized_obj,
    }
    return HttpResponse(json.dumps(response), content_type="application/json")
