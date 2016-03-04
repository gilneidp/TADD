#!/usr/bin/env python
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
import socket

fluxos =TemporaryFlows.objects.all().filter(ip_src='10.0.0.7')
fopen = open('./portscan.log', 'a')
for i in fluxos:
  print i.ip_src, i.timestamp
  fopen.write('%s: %s:\n '%(i.ip_src, i.timestamp))









