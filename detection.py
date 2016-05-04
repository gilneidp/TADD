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
from django.db.models import Count, Avg
import django.db.models.query

from madapp import settings
from madapp.mad.models import *

import time
django.setup()

INTERVAL = 0.1


while True:
  config_MD = ConfigTable.objects.values('ex_mdDeteccao', 'block_seqPortas','block_numFluxos')
  for conf in config_MD:
      exec_md = conf['ex_mdDeteccao'] # Define intervalo de Exec do Script
      block_seq =  conf['block_seqPortas'] # Define sequencia de portas no PortScan a serem bloq.
      block_nunf = conf['block_numFluxos'] # Define Numero de Fluxos a Partir do mesmo IP 
  print exec_md
  print block_seq
  print block_nunf 
  pd_port = [] #Lista de portas Agrupadas
# padrao = []  
  pattern = [] #Lista com portas a sererem identificadas como Padrao
  ip_atacante = [] #Lista de Ips Atacantes
  swt_atacante = [] #Lista de Switches com ataques originados
  swt_port_atacante = [] #Lista de portas com ataques ofiginados
  ip_ant = 0 
  ptr = 0
# IDENTIFICA PORTSCAN
  fl = TemporaryFlows.objects.values('ip_src','ip_dst','dst_port').filter(dst_port__lt = 1024).annotate(num_ports = Count('dst_port')).order_by('ip_src')
  for x in fl:
       if (ip_ant == x['ip_src']and ptr==0):                   
	 pd_port.append(x['dst_port'])
         print x
         for k, g in groupby(enumerate(pd_port), lambda (i, x): i-x):
            pattern =  map(itemgetter(1), g)
         # Verifica se sequencia esta dentro do definido 
         if  len(pattern) > block_seq:
              ptr = 1
              # Se for maior que o definido:
              ip_atacante.append(x['ip_src']) # Adiciona o IP do atacante a uma lista
         else:
              ptr = 0
         ip_ant=x['ip_src']
       else:
         ip_ant=x['ip_src']
         ptr = 0
         del pattern[:]

# IDENTIFICA INSISTENCIA EM PORTA/FLUXOS
  timeisnow=datetime.datetime.now() - timedelta(minutes=1)
  temps = TemporaryFlows.objects.values ('id_switch','switchport','ip_src','ip_dst', 'dst_port').filter(dst_port__lte='10024').annotate(num_ports=Count('dst_port'))
#  tempd = TemporaryFlows.objects.values ('id_switch','switchport','ip_src','ip_dst', 'src_port').annotate(num_ports=Count('src_port'))
  counter = 0
  for flow in temps:
     counter1 = flow['num_ports']
# for flow in tempd:
#    counter2 = flow['num_ports']
# Se Numero de fluxos for maior que o estabelecido
     if (counter > block_nunf): # verifica se ha varias tentativas na mesma porta
        swt_atacante.append(flow['id_switch'])
        swt_port_atacante.append(flow['switchport'])
#     rt = RuleTable(id_switch=switches, switchport = inport, ip_src = packet.next.srcip,
#              ip_dst = packet.next.dstip, src_port = sport, dst_port = dport, timestamp = datetime.datetime.now(), idle_timeout=3000, hard_timeout=20000, action='DST_HONEYPOT')
   #   rt.save()
     else:
    	 attack = 0


  flows = TemporaryFlows.objects.all()
  for flow in flows:
      collectedflows =StatsTable(id_switch = flow.id_switch, switchport = flow.switchport, ip_src = flow.ip_src, ip_dst = flow.ip_dst, src_port = flow.src_port, dst_port = flow.dst_port, timestamp = timezone.now())
      collectedflows.save()
  dl_temp = TemporaryFlows.objects.all().delete()
  time.sleep(exec_md)

