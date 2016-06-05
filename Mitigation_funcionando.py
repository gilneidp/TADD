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
  max_id = RuleTable.objects.values('id_rule').aggregate(Max('id_rule'))
  ID_ATUAL = max_id['id_rule__max']
  for rule in rules:
      if rule.action == 'DROP':
         os.system("sudo ovs-ofctl add-flow " + rule.id_switch.name_switch + " dl_type=0x0800,ip_src=" + rule.ip_src + 
                   ",ip_dst=" + rule.ip_dst + ",priority=65535,actions=drop")
      else:
         for i in swt:    
        	 os.system("sudo ovs-ofctl add-flow " + rule.id_switch.name_switch + " dl_type=0x0800,in_port="+str(rule.switchport)+",ip_src=" + rule.ip_src + ",ip_dst=" + rule.ip_dst + ",priority=65534,actions=mod_nw_dst:10.0.0.1,output:all")
        	 os.system("sudo ovs-ofctl add-flow " + rule.id_switch.name_switch + " dl_type=0x0800,ip_src=10.0.0.1,ip_dst=" + rule.ip_src +",actions=mod_nw_src:"+rule.ip_dst+",output:all")
#		 os.system("sudo ovs-ofctl add-flow " + rule.id_switch.name_switch + " dl_type=0x0800,ip_src=10.0.0.1,ip_dst=" + rule.ip_src + ",out_port=" + str(rule.switchport) + ",priority=65534,actions=mod_nw_src:"+rule.ip_dst+",output:all")
#                   ",ip_src=" + rule.ip_src + ",ip_dst=" + rule.ip_dst + ",Tp_dst="+ rule.dst_port + ",priority=65534,actions=Mod_nw_dst:10.0.0.1")
#  max_id = RuleTable.objects.values('id_rule').aggregate(Max('id_rule'))
#  ID_ATUAL = max_id['id_rule__max']
      hs_rules=HsTable(id_switch=rule.id_switch, switchport = rule.switchport, ip_src = rule.ip_src,
             ip_dst = rule.ip_dst, dst_port = rule.dst_port, idle_time=rule.idle_timeout, hard_time=rule.hard_timeout, 
	     action=rule.action, timestamp=timezone.now())
      hs_rules.save()
  dl_rules = RuleTable.objects.all().delete()

#  print ID_ATUAL


  time.sleep(exec_md)

