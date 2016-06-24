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
from django.db.models import Count, Avg, Max
import django.db.models.query

from madapp import settings
from madapp.mad.models import *

import time
django.setup()

INTERVAL = 0.1
ID_ATUAL = 0

while True:
  config_MD = ConfigTable.objects.values('ex_mdMitigacao')
  for conf in config_MD:
      exec_md = conf['ex_mdMitigacao'] # Define intervalo de Exec do Script
#  rules = RuleTable.objects.all().filter(id_rule__gt = ID_ATUAL)
  rules = RuleTable.objects.all()
  swt = Switches.objects.all()
  sw = []
  max_id = RuleTable.objects.values('id_rule').aggregate(Max('id_rule'))
  ID_ATUAL = max_id['id_rule__max']
  for rule in rules:
#     if rule.id_switch.name_switch not in swt:
#        sw.append(str(rule.id_switch.name_switch))
      if rule.action == 'DROP':
         os.system("sudo ovs-ofctl add-flow " + rule.id_switch.name_switch + " dl_type=0x0800,ip_src=" + rule.ip_src + 
                   ",ip_dst=" + rule.ip_dst + ",priority=65535,actions=drop")
      else:
      #  if rule.id_switch.name_switch not in swt:
      #     sw.append(str(rule.id_switch.name_switch))
        for i in swt:    
       	    os.system("sudo ovs-ofctl add-flow " + i.name_switch + " dl_type=0x0800,ip_src=" + rule.ip_src + ",ip_dst=" + rule.ip_dst + ",priority=65535,actions=mod_nw_dst:10.0.0.1,output:all")
#  os.system("sudo ovs-ofctl add-flow " + rule.id_switch.name_switch + " dl_type=0x0800,ip_dst=10.0.0.1,ip_src=" + rule.ip_src +",priority=65534,action=output:all")
  
            os.system("sudo ovs-ofctl add-flow " + i.name_switch + " dl_type=0x0800,ip_src=10.0.0.1,ip_dst=" + rule.ip_src +",priority=65535,actions=mod_nw_src:"+rule.ip_dst+",output:all")
#	    os.system("sudo ovs-ofctl add-flow " + i.name_switch + " dl_type=0x0800,ip_src=10.0.0.1,priority=65534,actions=output:all")
      # for i in sw:
       #        os.system("sudo ovs-ofctl add-flow " + i + " dl_type=0x0800,ip_src=" + rule.ip_src + ",ip_dst=10.0.0.1,actions=output:all")
       #        os.system("sudo ovs-ofctl add-flow " + i + " dl_type=0x0800,ip_src=" + rule.ip_dst + ",ip_dst=" + rule.ip_src +",actions=output:all")
      hs_rules=HsTable(id_switch=rule.id_switch, switchport = rule.switchport, ip_src = rule.ip_src,
             ip_dst = rule.ip_dst, dst_port = rule.dst_port, idle_time=rule.idle_timeout, hard_time=rule.hard_timeout, 
	     action=rule.action, timestamp=timezone.now())
      hs_rules.save()
  dl_rules = RuleTable.objects.all().delete()

#  print ID_ATUAL


  time.sleep(exec_md)

