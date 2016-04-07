import os
import sys
import datetime
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "madapp.settings")
from django.core.management import execute_from_command_line
from django.db.models import Count, Avg

from madapp import settings
from madapp.mad.models import *

import time

INTERVAL = 0.1


while True:
    flows = TemporaryFlows.objects.all()
    for flow in flows:
      collectedflows =StatsTable(id_switch = flow.id_switch, switchport = flow.switchport, ip_src = flow.ip_src, ip_dst = flow.ip_dst, src_port = flow.src_port, dst_port = flow.dst_port, timestamp = timezone.now())
      collectedflows.save()
    TemporaryFlows.objects.all().delete()
    time.sleep(60)

