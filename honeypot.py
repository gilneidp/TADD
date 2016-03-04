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

def GetPorts():
        motd = '$root# Welcome to the SDN Manager'
        host = '10.0.0.2'
#       port = [i for i in xrange(1024, 2048)]
        port = 6633
        return (host, port,  motd)
         
def writeLog(client, data=''):
        separator = '='*80
        fopen = open('./honeypot.log', 'a')
        fopen.write('Time: %s\nIP: %s\nPort: %d\nData: %s\n%s\n\n'%(time.ctime(), client[0], client[1], data, separator))
        fopen.close()

def main(host, port, motd):
            print 'Starting honeypot!'
            poxstats = UsageTable.objects.get(servername = 'HPN')
            poxstats.status = port
            poxstats.save()

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((host, port))
            s.listen(10000)

            while True:
                 (insock, address) = s.accept()
                 print 'Connection from: %s:%d' % (address[0], address[1])
                 try:
                         insock.send('%s\n'%(motd))
                         data = insock.recv(1024)
                         insock.close()
                 except socket.error, e:
                         writeLog(address)
                 else:
                         writeLog(address, data)
if __name__=='__main__':
        try:
                stuff = GetPorts()
                main(stuff[0], stuff[1], stuff[2])
        except KeyboardInterrupt:
                poxstats = UsageTable.objects.get(servername = 'HPN')
                poxstats.status = 0
                poxstats.save()
                print 'Bye!'
                exit(0)
        except BaseException, e:
                poxstats = UsageTable.objects.get(servername = 'HPN')
                poxstats.status = 0
                poxstats.save()

                print 'Error: %s' % (e)
                exit(1)
                                                          
