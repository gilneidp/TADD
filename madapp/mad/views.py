import os
import subprocess
import commands
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
    dtc_status = 9
    pox_status = 9
    mtd_status = 9
    script_pox = os.path.basename(__file__)
    script_detection = os.path.basename(__file__)
    l = commands.getstatusoutput("ps aux | grep -e '%s' | grep -v grep | awk '{print $2}'" % "pox.py")
    s = commands.getstatusoutput("ps aux | grep -e '%s' | grep -v grep | awk '{print $2}'" % "detection.py")
    r = commands.getstatusoutput("ps aux | grep -e '%s' | grep -v grep | awk '{print $2}'" % "mitigation.py")
    if l[1]:
            pox_status = 1
    else:
            pox_status = 0
    if s[1]:
            dtc_status = 1
    else:
            dtc_status = 0
    if r[1]:
            mtd_status = 1
    else:
            mtd_status = 0

    status = pox_status
    status_detection = dtc_status
    status_mitigation = mtd_status

    if (request.GET.get('opt_switch')): slc_switch = int(request.GET.get('opt_switch'))
    else: slc_switch = '1000'
    if ((slc_switch == 0) and (status == 1)):
       r = commands.getstatusoutput("pkill -f pox.py") 
       s = commands.getstatusoutput("pkill -f getresources.py")   
    elif ((slc_switch == 1) and (status == 0)):
       run_pox = os.path.basename(__file__)
       os.system("sudo python pox.py log --file=pox.log,w  forwarding.l3_learning &")
       os.system("sudo python getresources.py &")

    if (request.GET.get('opt_detection')): opt_detection = int(request.GET.get('opt_detection'))
    else: opt_detection = '1000'
    if ((opt_detection == 0) and (status_detection == 1)):
       r = commands.getstatusoutput("pkill -f detection.py")
    elif ((opt_detection == 1) and (status_detection == 0)):
       run_pox = os.path.basename(__file__)
       os.system("sudo python detection.py &")

    if (request.GET.get('opt_mitigation')): opt_mitigation = int(request.GET.get('opt_mitigation'))
    else: opt_mitigation = '1000'
    if ((opt_mitigation == 0) and (status_mitigation == 1)):
       r = commands.getstatusoutput("pkill -f mitigation.py")
    elif ((opt_mitigation == 1) and (status_mitigation == 0)):
       run_pox = os.path.basename(__file__)
       os.system("sudo python mitigation.py &")

    return render_to_response('index.html',
    RequestContext(request, {'status':status, 'status_detection':status_detection, 'status_mitigation':status_mitigation}))
def poxlogs(request):
    data_file = open('pox.log', 'r') #
    lista_logs = data_file.readlines()
    data = []

    for log in lista_logs:
        data.append(log)
    return render_to_response('poxlogs.html',
    RequestContext(request, {'data':data}))
def tempflows(request):
#    tempf = TemporaryFlows.objects.values ('id_switch','switchport','ip_src','ip_dst', 'dst_port').annotate(num_ports=Count('dst_port'))
    tempf = TemporaryFlows.objects.all()
    return render_to_response('tempflows.html',
    RequestContext(request, {'tempf':tempf}))
def installedflows(request):
    switches=Switches.objects.all().order_by('name_switch')
    if (request.GET.get('opt_switch')): slc_switch = int(request.GET.get('opt_switch'))
    else: slc_switch = '1000' 
    if ((slc_switch != 0) and (slc_switch != None)):
        flows = StatsTable.objects.all().order_by('stats_id').filter(id_switch=slc_switch)
    else:
       flows = StatsTable.objects.all().order_by('stats_id').reverse()
    return render_to_response('installedflows.html',RequestContext(request,{'flows':flows, 'switches':switches}))

def poxstatus(request):
    pox_status = 9
    script_name = os.path.basename(__file__)
    l = commands.getstatusoutput("ps aux | grep -e '%s' | grep -v grep | awk '{print $2}'" % "pox.py")
    if l[1]:
            #sys.exit(0);
            pox_status = 1
    else:
            pox_status = 0

    status = pox_status
    timeisnow= datetime.datetime.now() - timedelta(minutes=5)
    poxcpu = UsageTable.objects.filter(timestamp__gte=timeisnow, servername = 'POX_CTRL')
    time5=datetime.datetime.now() - timedelta(minutes=5)
    time4=datetime.datetime.now() - timedelta(minutes=4)
    time3=datetime.datetime.now() - timedelta(minutes=3)
    time2=datetime.datetime.now() - timedelta(minutes=2)
    time1=datetime.datetime.now() - timedelta(minutes=1)
    req1 =  StatsTable.objects.filter(timestamp__gte=time1).count()
    req2 =  StatsTable.objects.filter(timestamp__gte=time2).count() - req1
    req3 =  StatsTable.objects.filter(timestamp__gte=time3).count() - (req2 +req1)
    req4 =  StatsTable.objects.filter(timestamp__gte=time4).count() - (req3 + req2 +req1)
    req5 =  StatsTable.objects.filter(timestamp__gte=time5).count() - (req4 + req3 + req2 +req1)
    return render_to_response('poxstatus.html',
#    RequestContext(request, {'status':status, 'poxcpu':poxcpu, 'requests':requests}))
    RequestContext(request, {'status':status, 'poxcpu':poxcpu, 'req1':req1,'req2':req2,'req3':req3,'req4':req4,'req5':req5}))
def honeypotstatus(request):
    hpn_status = 9
    script_name = os.path.basename(__file__)
    l = commands.getstatusoutput("ps aux | grep -e '%s' | grep -v grep | awk '{print $2}'" % "honeypot.py")
    if l[1]:
            #sys.exit(0);
            hpn_status = 1
    else:
            hpn_status = 0

    hpnstatus = hpn_status
    data_file = open('honeypot.log', 'r') #
    data = data_file.readlines()   
    return render_to_response('honeypotstatus.html',
    RequestContext(request, {'hpnstatus':hpnstatus, 'data':data}))
def about(request):
    return render_to_response('about.html', context_instance=RequestContext(request))
def rules(request):
    switches=Switches.objects.all().order_by('name_switch')
    if (request.GET.get('opt_switch')): slc_switch = int(request.GET.get('opt_switch'))
    else: slc_switch = '1000'
    if ((slc_switch != 0) and (slc_switch != None)):
        rules = HsTable.objects.all().order_by('id_rule').filter(id_switch=slc_switch).reverse()
    else:
        rules = HsTable.objects.all().order_by('id_rule').reverse()
    return render_to_response('rules.html',RequestContext(request,{'rules':rules, 'switches':switches}))
