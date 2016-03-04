import os
import sys
import datetime
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "madapp.settings")
from django.core.management import execute_from_command_line

from django.db.models import Count, Sum, Max
from array import *
from django.db.models import F
from madapp import settings
from madapp.mad.models import *

import time
from datetime import timedelta
id_min = 0
timeisnow=datetime.datetime.now() - timedelta(hours = 14)
#temps = TemporaryFlows.objects.values('switchport','ip_src','ip_dst', 'dst_port').filter(timestamp__gte=timeisnow,dst_port__lte='10024').annotate(num_ports=Count('ip_src')).order_by('switchport')
portctr = TemporaryFlows.objects.values('switchport','ip_src','ip_dst').filter(timestamp__gte=timeisnow,dst_port__lte='10024').annotate(port_counter=Count('dst_port', distinct=True))
for x in portctr:
   print x['ip_src'], x['port_counter']
get_max = RuleTable.objects.all().aggregate(Max('id_rule'))
id_max = get_max['id_rule__max']
for x in portctr:
 while (id_min <= id_max):
   print x['ip_src'], x['port_counter']
   print id_max
   id_min=id_min+1

