from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
import hashlib, random, requests
from datetime import datetime, timedelta
from mails.models import Offer, BlackList
from django.core import serializers
import json

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
    offers = Offer.objects.filter(date__isnull=False)[0:5000]
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

    serialized_obj = serializers.serialize('json', BlackList.objects.all())
    return HttpResponse(serialized_obj, content_type="application/json")