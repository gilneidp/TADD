import os
import sys
import datetime
import django
import commands

from itertools import groupby
from operator import itemgetter
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "madapp.settings")
from django.core.management import execute_from_command_line
from django.db.models import Count, Avg
import django.db.models.query

from madapp import settings
from madapp.mad.models import *

import time
django.setup()

INTERVAL = 0.1


while True:
  ip
    fl = TemporaryFlows.objects.values('ip_src','ip_dst','dst_port').filter(dst_port__lt = 1024).annotate(num_ports = Count('dst_port'))
    padrao = []
    pattern = []
    for x in fl:
      padrao.append(x['dst_port'])
    for k, g in groupby(enumerate(padrao), lambda (i, x): i-x):
        pattern =  map(itemgetter(1), g)
        if  len(pattern) > 5:
          print 'Tem padrao!'
    flows = TemporaryFlows.objects.all()
    for flow in flows:
      collectedflows =StatsTable(id_switch = flow.id_switch, switchport = flow.switchport, ip_src = flow.ip_src, ip_dst = flow.ip_dst, src_port = flow.src_port, dst_port = flow.dst_port, timestamp = timezone.now())
      collectedflows.save()
    dl_temp = TemporaryFlows.objects.all().delete()
    time.sleep(20)

