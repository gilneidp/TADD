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
  rules = RuleTable.objects.all().filter(id_rule__gt = ID_ATUAL)
  max_id = RuleTable.objects.values('id_rule').aggregate(Max('id_rule'))
  ID_ATUAL = max_id['id_rule__max']
  for rule in rules:
      if rule.action == 'DROP':
         os.system("sudo Ovs-ofctl add-flow " + rule.id_switch.name_switch + " ip_src=" + rule.ip_src + 
                   ",ip_dst=" + rule.ip_dst +",priority=65535,actions=drop")
      else:
         os.system("sudo Ovs-ofctl add-flow " + rule.id_switch.name_switch + " in_port=" + rule.switch_port + 
                   ",ip_src=" + rule.ip_src + ",ip_dst=" + rule.ip_dst + ",Tp_dst="+ rule.dst_port+",priority=65534,actions=Mod_nw_dst:10.0.0.1")
#  max_id = RuleTable.objects.values('id_rule').aggregate(Max('id_rule'))
#  ID_ATUAL = max_id['id_rule__max']
  print ID_ATUAL


  time.sleep(exec_md)

