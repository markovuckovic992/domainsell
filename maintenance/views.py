from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse, render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout
import hashlib, random, requests, traceback
from datetime import datetime, timedelta
from mails.models import Offer, BlackList, controlPanel
from django.core import serializers
import json
from os import popen

def redirect(request):
    return render(request, '404.html')

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

            index = len(statuses) - 1 - statuses[::-1].index('Date:')
            try:
                date = datetime.strptime((statuses[index + 1])[0:10], '%Y-%m-%d').date()
            except:
                try:
                    date = datetime.strptime((statuses[index + 1])[0:11], '%d-%b-%Y').date()
                except:
                    date = None

            if 'pendingDelete' in str(statuses):
                if date:
                    Offer.objects.filter(id=offer.id).update(status=1, updated=date, phase=2, stage=1, done=0)
                else:
                    Offer.objects.filter(id=offer.id).update(status=1, updated=datetime.now().date(), phase=2, stage=1, done=0)
            else:
                Offer.objects.filter(id=offer.id).update(status=0)

        except:
            statuses = 'ERROR'
            msg += (traceback.format_exc() + '\n')
            Offer.objects.filter(id=offer.id).update(status=2)
        msg += ('DROP: ' + str(offer.drop) + str(statuses) + str(date))
        msg += '\n --------------------- \n'
    return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")

@csrf_exempt
def delete_old_data(request):
    offers = Offer.objects.filter(~Q(status=1), date__isnull=False)
    msg = ''
    for offer in offers:
        try:
            tube = popen("whois '" + str(offer.drop) + "' | egrep -i 'Status|Updated Date'", 'r')
            resp = tube.read()
            resp = resp.replace('Status:', '').replace('\n', '').replace('\r', '')
            tube.close()
            statuses = resp.split(' ')


            index = len(statuses) - 1 - statuses[::-1].index('Date:')
            try:
                date = datetime.strptime((statuses[index + 1])[0:10], '%Y-%m-%d').date()
            except:
                date = None

            if 'pendingDelete' in str(statuses):
                if date:
                    Offer.objects.filter(id=offer.id).update(status=1, updated=date)
                else:
                    Offer.objects.filter(id=offer.id).update(status=1, updated=datetime.now().date())
            else:
                Offer.objects.filter(id=offer.id).update(status=0)

        except:
            statuses = 'ERROR'
            msg += (traceback.format_exc() + '\n')
            Offer.objects.filter(id=offer.id).update(status=2)
        msg += ('DROP: ' + str(offer.drop) + str(statuses) + str(date))
        msg += '\n --------------------- \n'

    date = datetime.now().date() - timedelta(days=20)
    hashes = serializers.serialize('json', Offer.objects.filter(date_started__lt=date, amount__isnull=True))
    Offer.objects.filter(date_started__lt=date, amount__isnull=True).delete()
    serialized_obj = serializers.serialize('json', BlackList.objects.all())
    response = {
        'hashes': hashes,
        'blk': serialized_obj,
    }
    return HttpResponse(json.dumps(response), content_type="application/json")

def start_post_release(request):
    id_ = request.POST['id']
    turn_off = Offer.objects.get(id=id_).phase
    if turn_off == 2:
        Offer.objects.filter(id=id_).update(phase=10, done=1)
    else:
        Offer.objects.filter(id=id_).update(phase=2, stage=1, done=0)
    return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")

def start_post_sale(request):
    id_ = request.POST['id']
    turn_off = Offer.objects.get(id=id_).phase
    if turn_off == 3:
        Offer.objects.filter(id=id_).update(phase=10, done=1)
    else:
        Offer.objects.filter(id=id_).update(phase=3, stage=1, done=0)
    return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")

@login_required
def del_hash(request):
    id_ = request.POST['id']
    Offer.objects.filter(id=id_).delete()
    return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")

@login_required
def change_amount(request):
    id_ = request.POST['id']
    amount = request.POST['amount']
    Offer.objects.filter(id=id_).update(amount=amount)
    return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")

@login_required
def control_panel(request):
    if 'type' not in request.GET.keys():
            return HttpResponseRedirect("/control_panel/?type=post_offer")        
    _type = request.GET['type']
    if _type == 'post_offer':
        settings = controlPanel.objects.filter(tip=1)
        tip = 1
    if _type == 'post_release':
        settings = controlPanel.objects.filter(tip=2)
        tip = 2
    if _type == 'post_sale':
        settings = controlPanel.objects.filter(tip=3)
        tip = 3
    return render_to_response('control_panel.html', {'settings': settings, 'tip': tip})

def save_settings(request):
    values = []
    values.append(request.POST['1'])
    values.append(request.POST['2'])
    values.append(request.POST['3'])
    values.append(request.POST['4'])
    values.append(request.POST['5'])
    values.append(request.POST['6'])
    values.append(request.POST['7'])
    values.append(request.POST['8'])
    values.append(request.POST['9'])
    values.append(request.POST['10'])
    values.append(request.POST['11'])
    values.append(request.POST['12'])

    tip = request.POST['tip']
    index = 1
    for value in values:
        if value != u'undefined':
            controlPanel.objects.filter(tip=tip, order=index).update(distance=int(value))
        index += 1
    return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")


# SEARCH
def search(request):
    return render(request, 'search.html', {})

def search_results(request):
    name_redemption = request.POST['drop_domain']
    name_zone = request.POST['zone_domain']
    datepicker = request.POST['datepicker']
    try:
        date = datetime.strptime(datepicker, '%d-%m-%Y').date()
        search_leads = RawLeads.objects.filter(
            name_zone__contains=name_zone,
            name_redemption__contains=name_redemption,
            date=date,
        )[0:200]
    except:      
        search_leads = RawLeads.objects.filter(
            name_zone__contains=name_zone,
            name_redemption__contains=name_redemption
        )[0:200]
    return render(request, 'search.html', {'search_leads': search_leads})