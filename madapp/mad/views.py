import os
import datetime
from django.shortcuts import render
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.db.models import Count, Avg
from array import *
from .models import *
from django.db.models import F
from datetime import timedelta
from django.utils import timezone
from django.core import serializers

@login_required(login_url='/accounts/login/')
def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))
def poxlogs(request):
    data_file = open('pox.log', 'r') #
    data = data_file.readlines()
    return render_to_response('poxlogs.html',
    RequestContext(request, {'data':data}))
def tempflows(request):
#    timeisnow=datetime.datetime.now() - timedelta(minutes=1)
#    tempf = TemporaryFlows.objects.values ('id_switch','switchport','ip_src','ip_dst', 'dst_port').filter(timestamp__gte=timeisnow).annotate(num_ports=Count('dst_port'))
    tempf = TemporaryFlows.objects.values ('id_switch','switchport','ip_src','ip_dst', 'dst_port')

    return render_to_response('tempflows.html',
    RequestContext(request, {'tempf':tempf}))
def installedflows(request):
    switches=Switches.objects.all()
    if (request.GET.get('opt_switch')): slc_switch = int(request.GET.get('opt_switch'))
    else: slc_switch = '1000' 
    if ((slc_switch != 0) and (slc_switch != None)):
        flows = TemporaryFlows.objects.all().order_by('id_temporaryflow').filter(id_switch=slc_switch)
    else:
       flows = TemporaryFlows.objects.all().order_by('id_temporaryflow').reverse()
    return render_to_response('installedflows.html',RequestContext(request,{'flows':flows, 'switches':switches}))

def poxstatus(request):
    timeisnow= datetime.datetime.now() - timedelta(minutes=10)
    status = UsageTable.objects.filter(servername = 'POX')
    poxcpu = UsageTable.objects.filter(timestamp__gte=timeisnow, servername = 'POX_CTRL')
#   requests = TemporaryFlows.objects.filter(timestamp|date:"h:i"__gte=timeisnow).annotate(flow_count=Count('id_temporaryflow'))
    time5='5'
    time4= '4'
    time3= '3'
    time2= '2'
    time1= '1'
    req1 =  TemporaryFlows.objects.all()
    req2 =  TemporaryFlows.objects.all()
    req3 =  TemporaryFlows.objects.all()
    req4 =  TemporaryFlows.objects.all()
    req5 =  TemporaryFlows.objects.all()

#    time5=datetime.datetime.now() - timedelta(minutes=5)
#    time4=datetime.datetime.now() - timedelta(minutes=4)
#    time3=datetime.datetime.now() - timedelta(minutes=3)
#    time2=datetime.datetime.now() - timedelta(minutes=2)
#    time1=datetime.datetime.now() - timedelta(minutes=1)
#    req1 =  TemporaryFlows.objects.filter(timestamp__gte=time1).count()
#    req2 =  TemporaryFlows.objects.filter(timestamp__gte=time2).count() - req1
#    req3 =  TemporaryFlows.objects.filter(timestamp__gte=time3).count() - (req2 +req1)
#    req4 =  TemporaryFlows.objects.filter(timestamp__gte=time4).count() - (req3 + req2 +req1)
#    req5 =  TemporaryFlows.objects.filter(timestamp__gte=time5).count() - (req4 + req3 + req2 +req1)
    return render_to_response('poxstatus.html',
#    RequestContext(request, {'status':status, 'poxcpu':poxcpu, 'requests':requests}))
    RequestContext(request, {'status':status, 'poxcpu':poxcpu, 'req1':req1,'req2':req2,'req3':req3,'req4':req4,'req5':req5}))
def honeypotstatus(request):
    hpnstatus = UsageTable.objects.filter(servername = 'HPN')
    data_file = open('honeypot.log', 'r') #
    data = data_file.readlines()   
    return render_to_response('honeypotstatus.html',
    RequestContext(request, {'hpnstatus':hpnstatus, 'data':data}))
def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))
def rules(request):
    rules = RuleTable.objects.all().order_by('id_rule').reverse()
    for rule in rules:
      if (rule.action == '0'):
	rule.action = 'DROP'
      else:
	rule.action = 'DST_TO_HONEYPOT'
    return render_to_response('rules.html',
    RequestContext(request, {'rules':rules}))

