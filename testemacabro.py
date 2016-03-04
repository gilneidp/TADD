#!/usr/bin/python2.7
import os
import sys
import datetime
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "madapp.settings")
from django.core.management import execute_from_command_line
from django.utils import timezone
from django.db.models import Count
from array import *
from django.db.models import F
from madapp import settings
from madapp.mad.models import *

inport=1
srcip="10.0.0.1"
dstip="10.0.0.8"
switch_rule=None

switches = Switches.objects.all().filter(id_switch=41)
for switch in switches:
  switch_rule = switch

print switch_rule.id_switch

#rules = RuleTable.objects.all().filter(id_switch=switches.id_switch,switchport = inport,ip_src = packet.next.srcip,ip_dst = packet.next.dstip)
rules = RuleTable.objects.all().filter(switchport = inport,ip_src = srcip,ip_dst = dstip)
#rules = RuleTable.objects.all()

for rule in rules:
  print rule
