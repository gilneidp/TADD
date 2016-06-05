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
      exec_md = conf['ex_mdMitigacao'] + (conf['ex_mdMitigacao']/2) # Define intervalo de Exec do Script
      print exec_md

  time.sleep(exec_md)

