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

def getTimeList():
    cpuStats = file("/proc/stat", "r").readline()
    columns = cpuStats.replace("cpu", "").split(" ")
    return map(int, filter(None, columns))

def deltaTime(interval):
    timeList1 = getTimeList()
    time.sleep(interval)
    timeList2 = getTimeList()
    return [(t2-t1) for t1, t2 in zip(timeList1, timeList2)]

def getCpuLoad():
    dt = list(deltaTime(INTERVAL))
    idle_time = float(dt[3])
    total_time = sum(dt)
    load = 1-(idle_time/total_time)
    return load


while True:
#    print "CPU usage=%.2f%%" % (getCpuLoad()*100.0)
    poxstats = UsageTable(servername = 'POX_CTRL', cpu_usage = (getCpuLoad()*100.0), timestamp = timezone.now())
    poxstats.save()
    time.sleep(60)
