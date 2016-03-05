import os
import sys
import datetime
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "madapp.settings")
from django.core.management import execute_from_command_line
from django.db.models import Count, Avg

from madapp import settings
from madapp.mad.models import *

#imeisnow=datetime.datetime.now() - timedelta(minutes=1)
#lows = TemporaryFlows.objects.values ('switchport','ip_src','ip_dst', 'dst_port').filter(timestamp__gte=timeisnow).annotate(num_ports=Count('dst_port'))
#flows = TemporaryFlows.objects.all().order_by('id_temporaryflow').reverse()
#or flow in flows:
#  print flow['num_ports']
#  print 'hi'
#flows = TemporaryFlows.objects.get(pk=1)
#switchs = Switchs.objects.select_related().all()
#print (flows.id_switch.id_switch)
timeisnow=datetime.datetime.now() - timedelta(minutes=1)
tempfs = TemporaryFlows.objects.values ('switchport','ip_src','ip_dst', 'dst_port').filter(timestamp__gte=timeisnow, dst_port__lt=1024).annotate(num_ports=Count('dst_port'))
padrao =[]
for x in tempfs:
  padrao.append(x['dst_port'])
# print x['ip_src'], x['dst_port']
  portas = range(min(padrao),max(padrao))
  if len(padrao) < 5:
   print 'Nao tem padrao' 
  for c in range(0,len(padrao)-5):
    result = list(filter(lambda n: n in padrao[c:c+5],portas))
    if len(result) == 5:
      print 'Tem padrao!'
